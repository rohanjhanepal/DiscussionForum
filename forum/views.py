from django.shortcuts import render , redirect
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from . import models
from . import forms


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
    posts = models.Post.objects.all().order_by('-posted_on')
    context = {
        'categories': categories,
        'posts': posts,
        
    }
    return render(request, 'forum/index.html' , context=context)

def post_detail(request, slug): #post detail view for viewing post using slug
    post = models.Post.objects.filter(slug=slug).first()
    post.views += 1
    post.save()
    context = {
        'post': post,
    }
    return render(request, 'forum/post.html', context=context)

def search(request):
    if request.method == 'GET':
        query = request.GET['q']
        posts = models.Post.objects.filter(title__icontains=query)
        context = {
            'posts': posts,
            'query': query,
        }
        return render(request, 'forum/search.html', context=context)
    messages.error(request, 'You have to enter a search query')
    return redirect('forum:home')


def upvote(request,**kwargs):
    answer = models.Answer.objects.get(id=kwargs['id'])
    user = request.user

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

