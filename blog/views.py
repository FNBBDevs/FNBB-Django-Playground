from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post, Like, Comment
from .forms import CreatePostForm, UpdatePostForm, bounded_update_form, CommentForm, bounded_comment_form
import datetime

UPDATE_SOURCE = None
LIKE_SOURCE   = None

def home(request):
    if request.user.is_authenticated:
        likes = [like.post for like in Like.objects.all() if str(like.user) == str(request.user)]
        posts = list(Post.objects.order_by('-date').all())
        true_likes = [post.key in likes for post in posts]
        posts = [{'post':post, 'liked':like } for post,like in zip(posts, true_likes)]
        context = {
            'posts': posts,
            'title': 'Home'
        }
        return render(request=request, template_name="blog/home.html", context=context)
    else:
        return render(request=request, template_name='blog/welcome.html', context={'title': 'Welcome'})

def about(request):
    context = {
        'title': 'About'
    }
    return render(request, 'blog/about.html', context)

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
            'title': 'Welcome'
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
            'form': form,
            'title': 'Create Post'
        }
        return render(request, 'blog/create.html', context)

@login_required
def update(request, key):
    global UPDATE_SOURCE
    source = 'UPDATE-HOME' if 'home' in str(request.META['HTTP_REFERER']) else 'UPDATE-PROFILE'
    if not UPDATE_SOURCE:
        UPDATE_SOURCE = source
    print(f"[UPDATE] SOURCE of value: {UPDATE_SOURCE}")
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

            if UPDATE_SOURCE == 'UPDATE-HOME':
                UPDATE_SOURCE = None
                return redirect('blog-home')
            else:
                UPDATE_SOURCE = None
                return redirect('profile')
    else:
        post_to_edit = Post.objects.filter(key=key).values()[0]
        request_user = str(request.user)
        post_user    = str(post_to_edit['author'])
        if post_user == request_user:

            form = bounded_update_form(request=request, key=key)
            context = {
                'form': form,
                'key': key,
                'title': 'Update Post'
            }
            return render(request, 'blog/update.html', context)
        else:
            if UPDATE_SOURCE == 'UPDATE-HOME':
                return redirect('blog-home')
            else:
                return redirect('profile')

@login_required
def delete(request, key):
    source = str(request.META['HTTP_REFERER'])

    post_to_delete = Post.objects.order_by('-date').filter(key=key)

    request_user = str(request.user)
    post_user = str(post_to_delete.values()[0]['author'])

    if post_user == request_user:

        # get all the likes for this post
        # and remove the likes from the table
        try:
            post_likes = Like.objects.filter(post=post_to_delete.values()[0]['key'])
            post_likes.delete()
        except:
            pass

        post_to_delete.delete()
    
    if 'home' in source:
        return redirect('blog-home')
    else:
        return redirect('profile')
    
@login_required
def like(request, key):
    global LIKE_SOURCE
    source = [val for val in str(request.META['HTTP_REFERER']).split('/') if val != '']
    LIKE_SOURCE = 'LIKE-HOME' if (len(source) == 2 or ('home' in source)) else 'LIKE-COMMENT-VIEW'
    
    print(f"[LIKE] incoming like from raw source {source}")
    print(f"[LIKE] calculated source {LIKE_SOURCE}")
    
    # get the post by the key
    post = Post.objects.filter(key=key)

    # check if this user has liked the post
    # if so delete the like and decrease the
    # posts likes, else create a new like and
    # increase the posts likes.
    if existing_like := Like.objects.filter(user=str(request.user)).filter(post=key):
        key = existing_like.values()[0]['key']
        existing_like.delete()
        post.update(likes=post.values()[0]['likes'] - 1)
        try:
            tmp = Like.objects.get(key=key)
            print("[DELETE] error, like not deleted from database table")
        except:
            print("[DELETE] like deleted from the database table")
    else:
        new_like = Like(
            user = str(request.user),
            post = key
        )
        new_like.save()
        post.update(likes=post.values()[0]['likes'] + 1)
    if LIKE_SOURCE == 'LIKE-HOME':
        return redirect('blog-home')
    else:
        return redirect(reverse('post-view', args=(post.values()[0]['key'],)))

def view_post(request, key):
    post = Post.objects.filter(key=key).values()[0]
    form = CommentForm()
    current_comments = Comment.objects.order_by('-date').filter(post=key).values()
    user_comments    = [None if comment['user'] != str(request.user) else comment for comment in current_comments]
    print(current_comments)
    print(user_comments)
    liked = Like.objects.filter(user=request.user, post=key).values()
    
    context = {
        'post': post,
        'form': form,
        'comments': current_comments,
        'liked': True if liked else False
    }
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.cleaned_data['comment']
            comment = Comment(
                post=key,
                user=request.user,
                comment=new_comment,
                date=datetime.datetime.now()
            )
            comment.save()
        return render(request, 'blog/view_post.html', context=context)
    else:
        return render(request, 'blog/view_post.html', context=context)
