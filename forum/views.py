from unicodedata import category
from django.shortcuts import render , redirect
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from . import models
from . import forms
from . import recommendmodel as recommend
from . import advanced_search 
import os

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Welcome,{}'.format(username))
            return redirect('forum:home')
        else:
            messages.error(request, 'Something wrong with your username or password')
            return redirect('forum:login')
    else:

        return render(request, 'forum/login.html')

def signup_view(request):
    form = forms.Create_user_form(request.POST or None)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user = User.objects.get(username=form.cleaned_data.get('username'))
        profile = models.Profile(user=user)
        profile.first_name = form.cleaned_data['first_name']
        profile.last_name = form.cleaned_data['last_name']
        profile.gender = form.cleaned_data['gender']
        profile.save()
        form = forms.Create_user_form()
        messages.success(request, 'Account created successfully')
        redirect('forum:login')
    else:
        messages.error(request,"Error occoured , retry")
    context = {
        'form' : form
    }
    return render(request, 'forum/signup.html',context=context)

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('forum:home')

def index(request): #home page of discussion forum
    categories = models.Category.objects.all()
    posts = models.Post.objects.order_by('-posted_on','views')

    select = dict()
    for i in categories:
        select[i.name] = [j.name for j in i.subcategory.all()]
    

    if request.user.is_authenticated:
        user = User.objects.filter(username=request.user.username).first()
        profile = models.Profile.objects.filter(user=user).first()
        if profile.prefered_categories.all().__len__() != 0:
            posts = posts.filter(category__in=profile.prefered_categories.all())

    context = {
        'categories': categories,
        'posts': posts,
        'selects':select,
        
    }
    return render(request, 'forum/index.html' , context=context)


def recommend_questions(request):
    user = request.user
    pref_sub = user.profile.prefered_categories.all()
    posts = models.Post.objects.filter(solved=False)
    posts_solved = models.Post.objects.filter(category__in = pref_sub)
    context = {
        'posts':posts,
        'solved_posts':posts_solved,

    }
    return render(request, "forum/question_recommend.html",context = context)

def post_detail(request, slug): #post detail view for viewing post using slug
    post = models.Post.objects.filter(slug=slug).first()
    post.views += 1
    post.save()
    try:
        recommended = recommend.recommend_pro(int(post.id))
        recommended = recommended[:4]
        recommended_posts = models.Post.objects.filter(id__in=recommended)
    except :
        recommended_posts = []
        rp= models.Post.objects.all()
        for i in rp:
            if i.category.name == post.category.name:
                recommended_posts.append(i)


    if request.user.is_authenticated:
        
        user = User.objects.filter(username=request.user.username).first()
        
        profile = models.Profile.objects.filter(user=user).first()
        print("--------"+ profile.first_name)
        if post.category not in profile.prefered_categories.all():
            profile.prefered_categories.add(post.category) #.remove(post.category) to remove
            profile.save()
            
    context = {
        'post': post,
        'answers': post.answer.all().order_by('-upvotes'),
        'recommended_posts': recommended_posts,
    }
    return render(request, 'forum/post.html', context=context)

def search(request):
    if request.method == 'GET':
        query = request.GET['q']
        if query:
            terms = advanced_search.search(query)
            posts_list = set()
            for i in terms:
                all_res = models.Post.objects.filter(title__icontains=i)
                
                for j in all_res:
                    posts_list.add(j)
                
                try:
                    all_cat = models.Category.objects.filter(name__icontains=i).first()
                    cat = all_cat.post_category.all()
                    for k in cat:
                        posts_list.add(k)
                except:
                    pass
            posts = list(posts_list)
            if posts.__len__() == 0:
                messages.error(request, 'Enter a valid search query')
                return redirect('forum:home')
            context = {
                'posts': posts,
                'query': query,
            }
            return render(request, 'forum/search.html', context=context)
    messages.error(request, 'You have to enter a search query')
    return redirect('forum:home')

def category_view(request,id):
    categories = models.Category.objects.filter(id=id).first()
    post = categories.post_category.all()
    
    context = {
        'posts': post,
        'category': categories,
    }
    return render(request, 'forum/category.html', context=context)
def sub_category_view(request,id):
    categories = models.SubCategory.objects.filter(id=id).first()
    post = categories.post_sub_category.all()
    
    context = {
        'posts': post,
        'category': categories,
    }
    return render(request, 'forum/category.html', context=context)

def upvote(request,**kwargs):
    answer = models.Answer.objects.get(id=kwargs['id'])
   
    post = answer.post
    if request.user.is_authenticated:
       
        user = User.objects.filter(username=request.user.username).first()
        
        profile = models.Profile.objects.filter(user=user).first()
        
        if post.category not in profile.prefered_categories.all():
            profile.prefered_categories.add(post.category) #.remove(post.category) to remove
            profile.save()
    if models.Upvote.objects.filter(answer=answer , user=user).exists():
        pass
    else:
        upv = models.Upvote(user=user, answer=answer)
        upv.save()
    
    messages.success(request,"{}, thanks for upvoting".format(request.user.username))
    return redirect('forum:post_detail',slug=post.slug)

def solved(request,slug):
    post = models.Post.objects.get(slug=slug)
    if(not post.solved):
        post.solved = True
    else:
        post.solved = False
    post.save()
    return redirect('forum:post_detail',slug=slug)


def answer_view(request,slug):
    
    post = models.Post.objects.get(slug=slug)
    if request.method == 'POST':
        answer = request.POST['answer']
        
        if answer:
            ans = models.Answer(posted_by=request.user, post=post, answer=answer)
            ans.save()
            notify = models.Notification(post=post, answer=ans,to_user=post.posted_by)
            notify.save()
            messages.success(request, 'Answer posted successfully')
            os.system("python systemUtils.py")
            return redirect('forum:post_detail', slug=slug)
        messages.error(request, 'You have to enter an answer')
    return redirect('forum:post_detail', slug=slug)

@login_required
def notification_view(request):
    noti = models.Notification.objects.filter(to_user=request.user).order_by('-on')
    context= {'notifications':noti}
    return render(request, 'forum/notifications.html',context=context)


@login_required
def post_question(request):
    category_list = models.Category.objects.all()
    sub = models.SubCategory.objects.all()
    if request.method == 'POST':
        question = request.POST['question']
        category = request.POST['category']
        sub_category = request.POST['sub_category']
        if question and category:
            for  i in category_list:
                if i.name == category:
                    cat = i
            for i in sub:
                if i.name == sub_category:
                    sub_cat = i
            post = models.Post(posted_by=request.user, title=question, category=cat, subcategory=sub_cat)
            post.save()
            messages.success(request, 'Question posted successfully')
            os.system("python systemUtils.py")
            return redirect('forum:post_detail', slug=post.slug)
        messages.error(request, 'You have to enter a question')
    return redirect('forum:home')
        

