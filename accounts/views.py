from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from .forms import SignUpForm, EditProfileForm, ChangePasswordForm
from django.contrib.auth.decorators import login_required


def login_user(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Jste přihlášen/a.')
            return redirect('actions:home')
        else:
            messages.success(request, 'Přihlášení se nezdařilo.')
            return redirect('accounts:login_user')
    else:
        return render(request, 'registration/login.html', {})


@login_required()
def logout_user(request):
    logout(request)
    messages.success(request, 'Odhlášení proběhlo úspěšně.')
    return redirect('accounts:login_user')


def register_user(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registrace proběhla úspěšně.')
            return redirect('accounts:login_user')
    else:
        form = SignUpForm()

    context = {'form': form}
    return render(request, 'registration/registration.html', context=context)


@login_required()
def show_profile(request):
    context = {}
    return render(request, 'accounts/profile.html', context)


@login_required()
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Změna údajů proběhla úspěšně.')
            return redirect('accounts:profile')
    else:
        form = EditProfileForm(instance=request.user)

    context = {'form': form}
    return render(request, 'accounts/edit_profile.html', context)


@login_required()
def change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Změna hesla proběhla úspěšně.')
            return redirect('accounts:profile')
    else:
        form = ChangePasswordForm(user=request.user)

    context = {'form': form}
    return render(request, 'accounts/change_password.html', context)
