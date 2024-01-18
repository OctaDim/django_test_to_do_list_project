from django.shortcuts import render, redirect  # Changed
from django.contrib.auth import authenticate  # Added
from django.contrib.auth.models import auth  # Added

from apps.user.forms import LoginForm, CreateNewUserForm


# Create your views here.

def user_login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(
                request=request,
                username=username,
                password=password
            )

            if user is not None:
                auth.login(request, user=user)

                return redirect('router:tasks:get-all-tasks')

    context = {
        "form": form
    }

    return render(
        request=request,
        template_name='user_login_form.html',
        context=context
    )


# def create_new_user(request):
#     form = CreateNewUserForm()

    # if request.method == "POST"
