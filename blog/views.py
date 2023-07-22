from typing import Optional
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

import datetime
import warnings
warnings.filterwarnings('ignore')

from .models import Post, Like, Comment, Friend, Notification, FriendRequest
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

    posts = Post.objects.order_by('-date').all()

    # a True/False list to indicate whether the user has liked 'this' post
    true_likes = [post in user_likes for post in posts]

    posts = [{'post':post, 'liked':like } for post, like in zip(posts, true_likes)]

    try:
        notifications = Notification.objects.order_by('-date').filter(user_to_notify=request.user).filter(viewed=0).all()
    except Exception as exception:
        notifications = None

    try:
        frs = FriendRequest.objects.filter(to_user=request.user).all()
    except Exception as exception:
        frs = None

    if not posts:
        messages.add_message(request, messages.INFO, "Looks like there aren't any posts yet.")

    context = {
        'title': 'Home',
        'posts': posts,
        'notifications': notifications,
        'friend_requests': frs
    }

    return render(request=request, template_name="blog/home.html", context=context)

def about(request):
    """
    Function to render out the request page.
    """

    try:
        notifications = Notification.objects.order_by('-date').filter(user_to_notify=request.user).filter(viewed=0).all()
    except Exception as exception:
        notifications = None
    try:
        frs = FriendRequest.objects.filter(to_user=request.user).all()
    except Exception as exception:
        frs = None

    context = {
        'title': 'About',
        'notifications': notifications,
        'friend_requests': frs
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
            post = Post(
                author=request.user,
                title=form.cleaned_data['title'],
                content=form.cleaned_data['content'],
                date=datetime.datetime.now()
            ).save()

            return redirect('blog-home')
    else:
        try:
            notifications = Notification.objects.order_by('-date').filter(user_to_notify=request.user).filter(viewed=0).all()
        except Exception as exception:
            notifications = None
        try:
            frs = FriendRequest.objects.filter(to_user=request.user).all()
        except Exception as exception:
            frs = None

        form = CreatePostForm()
        context = {
            'title': 'Create Post',
            'form': form,
            'notifications': notifications,
            'friend_requests': frs
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

        try:
            notifications = Notification.objects.order_by('-date').filter(user_to_notify=request.user).filter(viewed=0).all()
        except Exception as exception:
            notifications = None
        try:
            frs = FriendRequest.objects.filter(to_user=request.user).all()
        except Exception as exception:
            frs = None

        post_to_edit = Post.objects.filter(key=key).first()
        if request.user.username == post_to_edit.author.username:
            form = UpdatePostForm(instance=post_to_edit)
            context = {
                'form': form,
                'key': key,
                'title': 'Update Post',
                'notifications': notifications,
                'friend_requests': frs
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
        next = redirect(reverse('post-view', args=(key,))) if '/view' in request.META.get('HTTP_REFERER', '/') else redirect('/blog/home/')
    except:
        next = redirect('/blog/home/')

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

    try:
        notifications = Notification.objects.order_by('-date').filter(user_to_notify=request.user).filter(viewed=0).all()
    except Exception as exception:
        notifications = None
    
    try:
        frs = FriendRequest.objects.filter(to_user=request.user).all()
    except Exception as exception:
        frs = None

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
        'title': f'{post.title}',
        'post': post,
        'form': form,
        'comments': comments,
        'liked': liked,
        'notifications': notifications,
        'friend_requests': frs
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
        friends = Friend.objects.filter(user=request.user).filter(friends_with=user_to_view).first()
        if friends: friends = True
        else: friends = False
    except Exception as exception:
        messages.warning(request, exception)
        friends = False

    try:
        users_likes = Like.objects.filter(user=user_to_view)
    except:
        pass

    try:
        notifications = Notification.objects.order_by('-date').filter(user_to_notify=request.user).filter(viewed=0).all()
    except Exception as exception:
        notifications = None
    
    try:
        frs = FriendRequest.objects.filter(to_user=request.user).all()
    except Exception as exception:
        frs = None

    context = {
        'posts': posts,
        'user_to_view': user_to_view,
        'friends': friends,
        'notifications': notifications,
        'friend_requests': frs
    }

    print(context)

    return render(request, template_name='blog/view_user.html', context=context)

@login_required
def add_friend(request, key):
    try:
        user_to_add = User.objects.filter(id=key).first()
        friends = Friend.objects.filter(user=request.user).all()
        if not friends:
            if FriendRequest.objects.filter(to_user=user_to_add).first():
                messages.info(request, 'You already ready sent a friend request to this user.')
                return redirect(reverse('view-user', args=(key,)))
            else:
                FriendRequest(
                    from_user = request.user,
                    to_user = user_to_add,
                    date = datetime.datetime.now()
                ).save()
                messages.info(request, f'A friend request has been sent to {user_to_add.username}')
                return redirect(reverse('view-user', args=(key,)))
        else:
            messages.info(request, 'You are already friends with this user.')
            return redirect(reverse('view-user', args=(key,)))
    except Exception as exception:
        print(exception)
        return redirect(reverse('view-user', args=(key,)))
    
@login_required
def remove_friend(request, key):
    try:
        friends = Friend.objects.filter(user=request.user).all()
        if friends:
            friends.delete()
        return redirect(reverse('view-user', args=(key,)))
    except Exception as exception:
        return redirect(reverse('view-user', args=(key,)))

@login_required
def clear_notification(request, key):
    try:
        Notification.objects.filter(key=key).update(viewed=1)
    except Exception as exception:
        pass
    return redirect('blog-home')

@login_required
def search(request):
    if request.method == "POST":
        try:
            notifications = Notification.objects.order_by('-date').filter(user_to_notify=request.user).filter(viewed=0).all()
        except Exception as exception:
            notifications = None
        
        try:
            frs = FriendRequest.objects.filter(to_user=request.user).all()
        except Exception as exception:
            frs = None

        query    = request.POST['query'].lower()
        posts    = Post.objects.all()
        users    = User.objects.all()
        comments = Comment.objects.all()

        posts = [post for post in posts if (query in post.content.lower() + post.title.lower() or query in post.title.lower())]
        users = [user for user in users if query in user.username.lower() ]
        comments = [comment for comment in comments if query in comment.comment.lower() + comment.user.username.lower()]
        context = {
            'query': query,
            'posts': posts,
            'users': users,
            'comments': comments,
            'notifications': notifications,
            'friend_requests': frs,
            'title': 'Search Results'
        }
    else:
        context = {
            'title': 'Search Results'
        }
    
    return render(request, template_name="blog/search.html", context=context)

@login_required
def autocomplete_search(request):
    query = request.GET.get('query')

    if query:

        posts = Post.objects.all()
        users  = User.objects.all()
        comments = Comment.objects.all()
        friends = [friend.friends_with.username 
                   for friend
                   in Friend.objects.filter(user=request.user).all()]

        posts = [post.content for post in posts if (
            (query in post.content.lower() or 
             query in post.title.lower()) 
            and (post.author.username in friends or 
                 post.author.profile.visibility == "Public" or 
                 post.author == request.user))]
        users = [user.username for user in users if query in user.username.lower() and user.profile.visibility == 'Public' ]
        comments = [comment.comment for comment in comments if query in comment.comment.lower()]

        return JsonResponse({'status': 200, 'data': users + posts + comments})
    else:
        return JsonResponse({'status': 200, 'data': []})
    
@login_required
def accept_friend_request(request, key1, key2):
    # check to make sure not friend TODO

    if request.user.id == key1:
        new_friend = Friend(
            user = request.user,
            friends_with = User.objects.filter(id=key2).first(),
            since = datetime.datetime.now()
        )
        new_friend.save()
        messages.success(request, "Friend has been added.")
    elif request.user.id == key2:
        new_friend = Friend(
            user = request.user,
            friends_with = User.objects.filter(id=key1).first(),
            since = datetime.datetime.now()
        )
        new_friend.save()
        messages.success(request, "Friend has been added.")
    else:
        messages.warning(request, 'Could not accept friend request.')
    
    return render(request, 'blog/home.html')
