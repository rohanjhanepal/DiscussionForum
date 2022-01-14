from django.shortcuts import render , redirect
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from . import models


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('forum:home')
        else:
            return redirect('forum:login')

    return render(request, 'forum/login.html')

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