from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm, MessageForm
# from .utils import searchProfiles, paginateProfiles

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import os


def user_login(request):
    if request.user.is_authenticated:
        # return redirect('profiles')
        return HttpResponse('welcome to profile')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)

        except User.DoesNotExist:
            messages.error(request, 'Username does not exits')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'books:product_list')

        else:
            messages.error(request, 'password does not match')

    return render(request, 'account/login_register.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('account:login')


def user_register(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'You have been registered')

            login(request, user)
            return redirect('books:product_list')

        else:
            messages.error(request, 'Please correct the error below')

    context = {'page': page, 'form': form}
    return render(request, 'account/login_register.html', context)


# def profiles(request):
#     profiles, search_query = searchProfiles(request)
#     custom_range, profiles = paginateProfiles(request, profiles, 1)

#     context = {'profiles': profiles,
#                'search_query': search_query,
#                'custom_range': custom_range}
#     return render(request, 'users/profiles.html', context)


def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)

    context = {'profile': profile}
    return render(request, 'account/user_profile.html', context)


@login_required(login_url='account:login')
def user_account(request):
    profile = request.user.profile
    products = profile.product_set.all()

    context = {'profile': profile, 'products': products}
    return render(request, 'account/account.html', context)


@login_required(login_url='account:login')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if 'profile_image' in request.FILES:
            if os.path.isfile(profile.profile_image.path):
                os.remove(profile.profile_image.path)

        if form.is_valid():
            form.save()
            return redirect('account:account')

    context = {'form': form}
    return render(request, 'account/profile_form.html', context)


@login_required(login_url='account:login')
def inbox(request):
    profile = request.user.profile
    messageRequest = profile.messages.all()
    unreadCount = messageRequest.filter(is_read=False).count()
    context = {'messageRequest': messageRequest, 'unreadCount': unreadCount}
    return render(request, 'account/inbox.html', context)


@login_required(login_url='account:login')
def view_message(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read is False:
        message.is_read = True
        message.save()

    context = {'message': message}
    return render(request, 'account/message.html', context)


def create_message(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile

    except Exception:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            messages.success(request, 'Message Was Sent succesfullly')
            return redirect('account:user_profile', pk=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request, 'account/message_form.html', context)
