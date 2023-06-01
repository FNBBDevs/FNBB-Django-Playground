from typing import Optional
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

import datetime
import warnings
warnings.filterwarnings('ignore')

from .models import Post, Like, Comment, Friend, Notification
from .forms import CreatePostForm, UpdatePostForm, CommentForm, UpdateCommentForm
from users.models import User

import bruhcolor

UPDATE_SOURCE = None
LIKE_SOURCE   = None

@login_required
def home(request):
    """
    Function to fetch the necessar data and render out the
    home page.
    """

    user_likes = [like.post for like in Like.objects.all() if like.user.username == request.user.username]
    print(user_likes)

    posts = Post.objects.order_by('-date').all()

    # a True/False list to indicate whether the user has liked 'this' post
    true_likes = [post in user_likes for post in posts]

    posts = [{'post':post, 'liked':like } for post, like in zip(posts, true_likes)]
    print(posts)

    try:
        notifications = Notification.objects.order_by('-date').filter(user_to_notify=request.user).filter(viewed=0).all()
    except Exception as exception:
        print(f"[HOME]: an error was encountered getting notifications:\n\t{exception}")
        notifications = None

    if not posts:
        messages.add_message(request, messages.INFO, "Looks like there aren't any posts yet.")

    context = {
        'title': 'Home',
        'posts': posts,
        'notifications': notifications
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
            try:
                notifications_to_delete = Notification.objects.filter(
                    notification_type='LIKE NOTIFICATION'
                    ).filter(
                    post=post.first()
                    ).filter(
                    user=request.user
                    ).delete()
            except Exception as exception:
                print(f"[LIKE POST]: An error occured deleting the notification:\n\t{exception}")
        else:
            new_like = Like(
                user = request.user,
                post = post.first()
            )

            try:
                Notification(
                    user = request.user,
                    user_to_notify = post.first().author,
                    notification_type = 'LIKE NOTIFICATION',
                    content = f'{request.user.username} liked your post "{post.first().title}".',
                    viewed = 0,
                    date = datetime.datetime.now(),
                    post = post.first()
                ).save()
            except Exception as exception:
                pass

            new_like.save()
            post.update(likes=post.first().likes + 1)

        return next
    except Exception as exception:
        messages.warning(request, "A problem was encountered. Could not like the post.")
        messages.warning(request, f"Additional Information: {exception}")
        return redirect('blog-home')

@login_required
def view_post(request, key):
    post = Post.objects.filter(key=key)

    if request.method == 'POST':
        comment = CommentForm(request.POST)
        if comment.is_valid():
            new_comment = Comment(
                post=post.first(),
                user=request.user,
                comment=comment.cleaned_data['comment'],
                date=datetime.datetime.now(),
                edited=0
            )
            new_comment.save()

            if new_comment.user != post.first().author:
                try:
                    Notification(
                        user = request.user,
                        user_to_notify = post.first().author,
                        notification_type = 'COMMENT NOTIFICATION',
                        content = f'{request.user.username} commented on your post "{post.first().title}".',
                        viewed = 0,
                        date = datetime.datetime.now(),
                        post = post.first()
                    ).save()
                except Exception as exception:
                    pass

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
            try:
                notifications_to_delete = Notification.objects.filter(
                        notification_type='COMMENT NOTIFICATION'
                        ).filter(
                        post=post.first()
                        ).filter(
                        user=request.user
                        ).delete()
            except:
                pass
        else:
            messages.warning(request, "You cannot delete a comment someone else created!") 
    except Exception as exception:
        messages.warning(request, f"Unable to delete comment. {exception}")

    return redirect(reverse('post-view', args=(postkey,)))

def view_user(request, key):

    if key == request.user.id:
        return redirect('profile')

    posts = Post.objects.filter(author=key).all()

    try:
        user_to_view = User.objects.filter(id=key).first()
    except Exception as e:
        messages.warning(request, "The requested user does not exist.")
        return redirect('blog-home')
    try:
        friends = Friend.objects.filter(user=request.user).filter(friends_with=key).first()
        if friends: friends = True
        else: friends = False
    except:
        friends = False

    try:
        users_likes = Like.objects.filter(user=user_to_view)
    except:
        pass
    
    context = {
        'posts': posts,
        'user_to_view': user_to_view
    }

    return render(request, template_name='blog/view_user.html', context=context)

@login_required
def add_friend(request, key):
    pass

def remove_friend(request, key):
    pass

def clear_notification(request, key):
    try:
        Notification.objects.filter(key=key).update(viewed=1)
    except Exception as exception:
        pass
    return redirect('blog-home')

