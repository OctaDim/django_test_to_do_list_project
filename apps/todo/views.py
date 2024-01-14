from django.shortcuts import render, redirect, get_object_or_404  # Changed

from apps.todo.models import User, Task, Category, Status  # Added
from apps.todo.forms import CreateTaskForm, TaskUpdateForm  # Added


# from django.http import HttpResponseRedirect  # Added


# Create your views here.


def home_page(request):
    return render(request=request,
                  template_name="main.html",  # full way, if not defined in setting DIR
                  )


def get_all_tasks(request):
    tasks = Task.objects.all()
    tasks_count = Task.objects.all().count()
    context = {"tasks": tasks,
               "task_count": tasks_count}
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

        # context = {"form": form,
        #            "users": users,
        #            "categories": categories,
        #            "statuses": statuses, }
    else:
        form = CreateTaskForm
        context = {"form": form,
                   "users": users,
                   "categories": categories,
                   "statuses": statuses, }
        return render(request=request,
                      template_name="create_task_form.html",
                      context=context)


def update_task_by_id(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # users = User.objects.all()
    categories = Category.objects.all()
    statuses = Status.objects.all()

    if request.method == "POST":
        form = TaskUpdateForm(request.POST,
                              instance=task)  # instance=task parameter initializes the form with the existing task data.

        if form.is_valid():
            form.save()
            return redirect("router:tasks:all-tasks")

        context = {"form": form,
                   "task": task,
                   # "users": users,
                   "categories": categories,
                   "statuses": statuses, }

    else:  # if request.method == "POST":
        form = TaskUpdateForm(
            instance=task)  # instance=task parameter initializes the form with the existing task data.

        context = {"form": form,
                   "task": task,
                   # "users": users,
                   "categories": categories,
                   "statuses": statuses, }

        return render(request=request,
                      template_name="update_task_form.html",
                      context=context)


def get_task_info_by_task_id(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    context = {"task": task, }

    return render(request=request,
                  template_name="get_task_info.html",
                  context=context)


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect("router:tasks:all-tasks")
