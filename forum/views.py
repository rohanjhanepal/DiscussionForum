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

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
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
    if request.user.is_authenticated:
        user = User.objects.filter(username=request.user.username).first()
        profile = models.Profile.objects.filter(user=user).first()
        if profile.prefered_categories.all().__len__() != 0:
            posts = posts.filter(category__in=profile.prefered_categories.all())

    context = {
        'categories': categories,
        'posts': posts,
        
    }
    return render(request, 'forum/index.html' , context=context)

def post_detail(request, slug): #post detail view for viewing post using slug
    post = models.Post.objects.filter(slug=slug).first()
    post.views += 1
    post.save()
    recommended = recommend.recommend_pro(int(post.id))
    recommended = recommended[:2]
    recommended_posts = models.Post.objects.filter(id__in=recommended)
    if request.user.is_authenticated:
        
        user = User.objects.filter(username=request.user.username).first()
        
        profile = models.Profile.objects.filter(user=user).first()
        print("--------"+ profile.first_name)
        if post.category not in profile.prefered_categories.all():
            profile.prefered_categories.add(post.category) #.remove(post.category) to remove
            profile.save()
            
    context = {
        'post': post,
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
        print("--------"+ profile.first_name)
        if post.category not in profile.prefered_categories.all():
            profile.prefered_categories.add(post.category) #.remove(post.category) to remove
            profile.save()
    if models.Upvote.objects.filter(answer=answer , user=user).exists():
        pass
    else:
        upv = models.Upvote(user=user, answer=answer)
        upv.save()
    
    
    return redirect('forum:home')

def solved(request,slug):
    post = models.Post.objects.get(slug=slug)
    if(not post.solved):
        post.solved = True
    post.save()
    return redirect('forum:home')

'''
@login_required
def post_question(request):
    if request.method == 'POST':
        form = forms.PostQuestionForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('forum:home')
    else:
        form = forms.PostQuestionForm()
    context = {
        'form': form
    }
    return render(request, 'forum/post_question.html', context=context)

'''