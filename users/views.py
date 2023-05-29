from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from blog.models import Post


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
        if request.method == 'POST':
            user_update_form = UserUpdateForm(request.POST, instance=request.user)
            profile_update_form = ProfileUpdateForm(request.POST, request.FILES,
                                                    instance=request.user.profile)
            
            if user_update_form.is_valid() and profile_update_form.is_valid():
                user_update_form.save()
                profile_update_form.save()
                messages.success(request, "Your profile has been updated successfully.")
                return redirect('profile')


        else:
            user_update_form = UserUpdateForm(instance=request.user)
            profile_update_form = ProfileUpdateForm(instance=request.user.profile)
            you = User.objects.get(username=request.user)
            your_posts = [post for post in Post.objects.all() if post.author==you.username]
            context = {
                'you': you,
                'posts': your_posts,
                'title': 'Profile',
                'user_update_form': user_update_form,
                'profile_update_form': profile_update_form
            }
        return render(request, 'users/profile.html', context)
