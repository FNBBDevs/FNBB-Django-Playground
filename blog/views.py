from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post, Like
from .forms import CreatePostForm, UpdatePostForm
import datetime

def home(request):
    if request.user.is_authenticated:
        likes = [like.post for like in Like.objects.all() if str(like.user) == str(request.user)]
        posts = list(Post.objects.order_by('-date').all())
        true_likes = [post.key in likes for post in posts]
        posts = [{'post':post, 'liked':like } for post,like in zip(posts, true_likes)]
        context = {
            'posts': posts,
        }
        return render(request=request, template_name="blog/home.html", context=context)
    else:
        return render(request=request, template_name='blog/welcome.html')

def about(request):
    return render(request, 'blog/about.html')

def welcome(request):
    if not request.user.is_authenticated:
        return render(request=request, template_name='blog/welcome.html')
    else:
        likes = [like.post for like in Like.objects.all() if str(like.user) == str(request.user)]
        posts = list(Post.objects.order_by('-date').all())
        true_likes = [post.key in likes for post in posts]
        posts = [{'post':post, 'liked':like } for post,like in zip(posts, true_likes)]
        context = {
            'posts': posts,
        }
        return render(request=request, template_name="blog/home.html", context=context)

@login_required
def create_post(request):
    if request.method == "POST":
        form = CreatePostForm(request.POST)
        if form.is_valid():
            new_post = Post(
                author=request.user,
                title=form.cleaned_data['title'],
                content=form.cleaned_data['content'],
                date=datetime.datetime.now()
            )
            new_post.save()
            return redirect('blog-home')
    else:
        form = CreatePostForm()
        context = {
            'form': form
        }
        return render(request, 'blog/create.html', context)

@login_required
def update(request, key):
    if request.method == "POST":
        form = UpdatePostForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            new_title = form['title']
            new_content = form['content']
            old_post = Post.objects.filter(key=key)
            if new_title != '':
                old_post.update(title=new_title)
            if new_content != '':
                old_post.update(content=new_content)
            return redirect('profile')
    else:
        request_user = str(request.user)
        post_user    = str(Post.objects.filter(key=key).values()[0]['author'])
        if post_user == request_user:

            form = UpdatePostForm()
            context = {
                'form': form,
                'key': key
            }
            return render(request, 'blog/update.html', context)
        else:
            return redirect('profile')

@login_required
def delete(request, key):
    source = str(request.META['HTTP_REFERER'])

    post_to_delete = Post.objects.filter(key=key)

    request_user = str(request.user)
    post_user = str(post_to_delete.values()[0]['author'])

    if post_user == request_user:
        post_to_delete.delete()
    
    if 'home' in source:
        return redirect('blog-home')
    else:
        return redirect('profile')
    
@login_required
def like(request, key):
    # get the post by the key
    post = Post.objects.filter(key=key)

    # check if this user has liked the post
    # if so delete the like and decrease the
    # posts likes, else create a new like and
    # increase the posts likes.
    if existing_like := Like.objects.filter(user=str(request.user)).filter(post=key):
        existing_like.delete()
        post.update(likes=post.values()[0]['likes'] - 1)
    else:
        new_like = Like(
            user = str(request.user),
            post = key
        )
        new_like.save()
        post.update(likes=post.values()[0]['likes'] + 1)
    return redirect('blog-home')

