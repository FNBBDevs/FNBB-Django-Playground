from typing import Optional
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

import datetime
import warnings
warnings.filterwarnings('ignore')

from .models import Post, Like, Comment
from .forms import CreatePostForm, UpdatePostForm, CommentForm, UpdateCommentForm

UPDATE_SOURCE = None
LIKE_SOURCE   = None

@login_required
def home(request):
    """
    Function to fetch the necessar data and render out the
    home page.
    """

    user_likes = [like.post for like in Like.objects.all() if like.user.username == request.user.username]

    posts = Post.objects.order_by('-date').all()

    # a True/False list to indicate whether the user has liked 'this' post
    true_likes = [post.key in user_likes for post in posts]

    posts = [{'post':post, 'liked':like } for post, like in zip(posts, true_likes)]

    if not posts:
        messages.add_message(request, messages.INFO, "Looks like there aren't any posts yet.")

    context = {
        'title': 'Home',
        'posts': posts
    }

    return render(request=request, template_name="blog/home.html", context=context)

def about(request):
    """
    Function to render out the request page.
    """
    context = {
        'title': 'About'
    }
    return render(request, 'blog/about.html', context)

def welcome(request):
    """
    Function to render out the welcome page for 
    unauthroized users.
    """
    
    if not request.user.is_authenticated:
        return render(request=request, template_name='blog/welcome.html')
    else:
        return home(request)

@login_required
def create_post(request):
    """
    Function to render out the create post page, and 
    handling of the create post form.
    """
    
    if request.method == "POST":
        form = CreatePostForm(request.POST)
        if form.is_valid():
            Post(
                author=request.user,
                title=form.cleaned_data['title'],
                content=form.cleaned_data['content'],
                date=datetime.datetime.now()
            ).save()
            return redirect('blog-home')
    else:
        form = CreatePostForm()
        context = {
            'title': 'Create Post',
            'form': form,
        }
        return render(request, 'blog/create_post.html', context)

@login_required
def update_post(request, key):
    next = request.POST.get('next', '/')
    if request.method == "POST":
        form = UpdatePostForm(request.POST)
        if form.is_valid():
            try:
                Post.objects.filter(key=key).update(
                    title=form.cleaned_data['title'],
                    content=form.cleaned_data['content']
                )
            except Exception as exception:
                messages.warning(request, f'A problem was encountered. Could not update post: {exception}')
                return redirect(next)
    else:
        post_to_edit = Post.objects.filter(key=key).first()
        if request.user.username == post_to_edit.author.username:
            form = UpdatePostForm(instance=post_to_edit)
            context = {
                'form': form,
                'key': key,
                'title': 'Update Post'
            }
            return render(request, 'blog/update_post.html', context)
    return redirect(next)

@login_required
def delete_post(request, key):
    try:
        next = '/home/' if '/home' in request.META.get('HTTP_REFERER', '/') else '/profile/'
    except:
        next = '/profile/'

    try:
        post_to_delete = Post.objects.order_by('-date').filter(key=key).first()
    except:
        messages.warning(request, "A problem was encountered. Post not deleted.")
        return redirect(next)

    if post_to_delete and post_to_delete.author.username == request.user.username:

        # delete associated likes
        try:
            post_likes = Like.objects.filter(post=key)
            post_likes.delete()
        except:
            pass
        
        # deleted associated comments
        try:
            post_comments = Comment.objects.filter(post=key)
            post_comments.delete()
        except:
            pass

        post_to_delete.delete()
    
    return redirect(next)
    
@login_required
def like_post(request, key):

    try:
        next = redirect(reverse('post-view', args=(key,))) if '/view' in request.META.get('HTTP_REFERER', '/') else redirect('/home/')
    except:
        next = redirect('/home/')

    try:
        post = Post.objects.filter(key=key)
    except:
        messages.warning(request, "A problem was encountered. Could not like post.")
        return redirect(next)
    
    try:
        if existing_like := Like.objects.filter(user=request.user).filter(post=key).first():
            key = existing_like.key
            existing_like.delete()
            post.update(likes=post.first().likes - 1)
        else:
            new_like = Like(
                user = request.user,
                post = key
            )
            new_like.save()
            post.update(likes=post.first().likes + 1)

        return next
    except Exception as exception:
        messages.warning(request, "A problem was encountered. Could not like the post.")
        messages.warning(request, f"Additional Information: {exception}")
        return redirect('blog-home')

@login_required
def view_post(request, key):
    post     = Post.objects.filter(key=key)

    if request.method == 'POST':
        comment = CommentForm(request.POST)
        if comment.is_valid():
            Comment(
                post=key,
                user=request.user,
                comment=comment.cleaned_data['comment'],
                date=datetime.datetime.now(),
                edited=0
            ).save()

            post.update(comments = post.first().comments + 1)

            return redirect(reverse('post-view', args=(key,)))

    post = post.first() 
    comments = [{'comment': comment, 'update_comment_form': UpdateCommentForm(instance=comment)} 
                for comment in Comment.objects.order_by('-date').filter(post=key).all()]
    form = CommentForm()
    try:
        if Like.objects.filter(user=request.user).filter(post=key):
            liked = True
        else:
            liked = False
    except:
        liked = False

    context = {
        'post': post,
        'form': form,
        'comments': comments,
        'liked': liked
    }
        
    return render(request, 'blog/view_post.html', context)

@login_required
def update_comment(request, commentkey, postkey):
    form = UpdateCommentForm(request.POST)
    if form.is_valid():
        form = form.cleaned_data
        new_comment = form['comment']
        try:
            comment_to_update = Comment.objects.filter(key=commentkey)
            if comment_to_update.first().user == request.user:
                same_comment = comment_to_update.first().comment == new_comment
                if not same_comment:
                    comment_to_update.update(comment=new_comment, date=datetime.datetime.now())
                if comment_to_update.first().edited == 0 and not same_comment:
                    comment_to_update.update(edited=1)
            else:
                messages.warning(request=request, message="You cannot update a comment that is not yours!")
        except Exception as exception:
            messages.warning(request=request, message="That comment does not exist!")
            messages.warning(request=request, message=f"Additional Information: {exception}")
    else:
        messages.warning(request=request, message="Could not update comment.")
    return redirect(reverse('post-view', args=(postkey,)))

@login_required   
def delete_comment(request, commentkey, postkey):
    try:
        comment_to_delete = Comment.objects.filter(key=commentkey).first()
        if request.user.username == comment_to_delete.user.username:
            comment_to_delete.delete()

            post = Post.objects.filter(key=postkey)
            post.update(comments=post.first().comments - 1)
        else:
            messages.warning(request, "You cannot delete a comment someone else created!") 
    except Exception as exception:
        messages.warning(request, f"Unable to delete comment. {exception}")

    return redirect(reverse('post-view', args=(postkey,)))