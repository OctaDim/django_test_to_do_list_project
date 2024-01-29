from django.shortcuts import render, redirect, get_object_or_404  # Changed
from django.contrib.auth import authenticate  # Added
from django.contrib.auth.models import auth  # Added
from django.contrib.auth.decorators import login_required  # Added Decorator password required

# ####################################################
# from django.contrib.auth.models import User  # Added
from apps.user.models import User
# ####################################################

from apps.user.forms import LoginForm, CreateNewUserForm  # Added

from apps.todo.models import Task, SubTask


# Create your views here.

def login_existing_user(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request=request,
                                username=username,
                                password=password)

            if user is not None:
                auth.login(request, user=user)

                return redirect('router:tasks:get-all-tasks')

    context = {"form": form, }

    return render(request=request,
                  template_name='login_existing_user_form.html',
                  context=context)


def register_new_user(request):
    form = CreateNewUserForm()

    if request.method == "POST":
        form = CreateNewUserForm(request.POST, )
        if form.is_valid():
            form.save()
            return redirect("router:user:login-existing-user")

    context = {"form": form, }

    return render(request=request,
                  template_name="register_new_user.html",
                  context=context)


@login_required(login_url="router:user:login-existing-user")
def user_profile_info(request):
    user = get_object_or_404(User, id=request.user.id)
    tasks = Task.objects.filter(creator=user.id)  # The same: creator=request.user.id
    subtasks = SubTask.objects.filter(creator=user.id)  # The same: creator=request.user.id

    context = {"user": user,
               "tasks": tasks,
               "subtasks": subtasks, }

    return render(request=request,
                  template_name="user_profile_info.html",
                  context=context)


def logout_user(request):
    auth.logout(request=request)
    return redirect("router:user:login-existing-user")
