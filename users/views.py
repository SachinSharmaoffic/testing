from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import forms
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User


# @login_required
# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request,
                f"Account Sucessfully created for {username}! Login Now to see the magic",
            )
            return redirect("base:home")

    else:
        form = UserCreationForm()
    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user

    context = {
        "user_profile": user.profile,
    }

    template_name = "users/profile.html"  # Specify your template name here

    return render(request, template_name, context)


def profile_update(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Account Updated Sucessfully")
            return redirect(profile)
    else:
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )

    context = {
        "u_form": u_form,
        "p_form": p_form,
    }
    return render(request, "users/profile_update.html", context)
