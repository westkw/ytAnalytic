from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserSubscriptionForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Channel
from django.contrib.auth.models import User

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account created!')
            return redirect('login')
    else:
        form = UserCreationForm()
    context = {
        'form' : form
    }
    return render(request, 'users/register.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserSubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            channel_id = form.cleaned_data.get('channel_id')
            print(channel_id)
            user = form.cleaned_data.get(request.user.username)
            # print(user)
            messages.success(request, 'Added Subscription!')
            return redirect('profile')
    else:
        form = UserSubscriptionForm()
    context = {
        'form' : form,
        'channels': Channel.objects.get(name=request.user.username)
    }
    return render(request, 'users/profile.html', context)