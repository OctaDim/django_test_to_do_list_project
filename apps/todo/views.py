from django.shortcuts import render, redirect  # Changed

from apps.todo.models import User, Task, Category, Status  # Added
from apps.todo.forms import CreateTaskForm  # Added


# Create your views here.


def home_page(request):
    return render(request=request,
                  template_name="main.html",  # full way, if not defined in setting DIR
                  )


def get_all_tasks(request):
    tasks = Task.objects.all()
    context = {"tasks": tasks, }
    return render(request=request,
                  template_name="all_tasks.html",  # full way, if not defined in setting DIR
                  context=context)


def create_new_task(request):
    users = User.objects.all()
    categories = Category.objects.all()
    statuses = Status.objects.all()

    if request.method == "POST":
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            task_data = form.cleaned_data
            Task.objects.create(**task_data)
            return redirect("router:tasks:all-tasks")

        context = {"form": form,
                   "users": users,
                   "categories": categories,
                   "statuses": statuses, }
    else:
        form = CreateTaskForm
        context = {"form": form,
                   "users": users,
                   "categories": categories,
                   "statuses": statuses, }
        return render(request=request,
                      template_name="create_task_form.html",
                      context=context)
