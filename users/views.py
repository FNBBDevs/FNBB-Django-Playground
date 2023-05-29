from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from blog.models import Post
from hashlib import sha1


def register(request):
    if request.method == 'POST':
        print(request.POST)
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            f = form.save()
            messages.success(request, f'Your account has been created. Please login.')
            return redirect('login')
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
        'title': 'Register'
    }
    return render(request, 'users/register.html', context)

@login_required
def profile(request):
        you = User.objects.get(username=request.user)
        your_posts = [post for post in Post.objects.all() if post.author==you.username]
        context = {
            'you': you,
            'posts': your_posts,
            'title': 'Profile'
        }
        return render(request, 'users/profile.html', context)
