from django.shortcuts import render, redirect, get_object_or_404  # Changed

from apps.todo.models import (User,
                              Task,
                              SubTask,
                              Category,
                              Status,
                              )  # Added

from apps.todo.forms import (CreateTaskForm,
                             TaskUpdateForm,
                             SubTaskUpdateForm,
                             CreateSubTaskForm,
                             )  # Added


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
               "task_count": tasks_count,
               }

    return render(request=request,
                  template_name="all_tasks.html",  # full way, if not defined in setting DIR
                  context=context)


def create_new_task(request):
    if request.method == "POST":
        form = CreateTaskForm(request.POST)

        if form.is_valid():
            task_data = form.cleaned_data
            Task.objects.create(**task_data)
            return redirect("router:tasks:all-tasks")

    else:  # if request.method == "GET":
        users = User.objects.all()
        categories = Category.objects.all()
        statuses = Status.objects.all()

        form = CreateTaskForm()

        context = {"form": form,
                   "users": users,
                   "categories": categories,
                   "statuses": statuses, }

        return render(request=request,
                      template_name="create_task_form.html",
                      context=context)


def update_task_by_id(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        form = TaskUpdateForm(request.POST,
                              instance=task)  # instance=task parameter initializes the form with the existing task data.

        if form.is_valid():
            form.save()
            return redirect("router:tasks:all-tasks")

    else:  # if request.method == "GET":
        form = TaskUpdateForm(
            instance=task)  # instance=task parameter initializes the form with the existing task data.

        categories = Category.objects.all()
        statuses = Status.objects.all()
        # users = User.objects.all()

        context = {"form": form,
                   "task": task,
                   # "users": users,
                   "categories": categories,
                   "statuses": statuses, }

        return render(request=request,
                      template_name="update_task_form.html",
                      context=context)


def get_task_by_task_id(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    subtasks = SubTask.objects.filter(task=task_id)

    context = {"task": task,
               "subtasks": subtasks, }

    return render(request=request,
                  template_name="task_info.html",
                  context=context)


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect("router:tasks:all-tasks")


def get_all_subtasks_by_creator(request):
    subtasks = SubTask.objects.filter(creator=request.user, )

    context = {"subtasks": subtasks, }

    return render(request=request,
                  template_name="all_subtasks.html",
                  context=context)


def get_subtask_by_id(request, subtask_id):
    subtask = get_object_or_404(SubTask, id=subtask_id)

    context = {"subtask": subtask, }

    return render(request=request,
                  template_name="subtask_info.html",
                  context=context)


def update_subtask_by_subtask_id(request, subtask_id):
    subtask = get_object_or_404(SubTask, id=subtask_id)

    if request.method == 'POST':
        form = SubTaskUpdateForm(request.POST, instance=subtask)

        if form.is_valid():
            form.save()
            return redirect('router:tasks:get-subtask-by-id', subtask_id=subtask_id)

    else:  # instance=task parameter initializes the form with the existing task data.
        form = SubTaskUpdateForm(instance=subtask)

        categories = Category.objects.all()
        statuses = Status.objects.all()

        context = {"form": form,
                   "subtask": subtask,
                   "categories": categories,
                   "statuses": statuses, }

        return render(
            request=request,
            template_name='update_subtask_form.html',
            context=context)


def create_new_subtask(request):
    task_id = request.GET.get("task_id")  # getting data via query from the request, not from reverse urls

    if request == "POST":
        form = CreateTaskForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("router:tasks:get-task", task_id=task_id)

    else:
        form = CreateSubTaskForm()

        task = get_object_or_404(Task, id=task_id)
        user = get_object_or_404(User, id=request.user.id)
        categories = Category.objects.all()
        statuses = Status.objects.all()

        context = {
            "form": form,
            "user": user,
            "task": task,
            "categories": categories,
            "statuses": statuses, }

        return render(request=request,
                      template_name="create_subtask_form.html",
                      context=context)

    # task_id = request.GET.get("task_id")
    #
    # if request.method == 'POST':
    #     form = CreateSubTaskForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('router:tasks:get-task', task_id=task_id)
    #
    # else:
    #     form = CreateSubTaskForm()
    #
    #     task = get_object_or_404(Task, id=task_id)
    #     user = get_object_or_404(User, id=request.user.id)
    #
    #     categories = Category.objects.all()
    #     statuses = Status.objects.all()
    #
    #     context = {"form": form,
    #                "user": user,
    #                "categories": categories,
    #                "statuses": statuses,
    #                "task": task, }
    #
    #     return render(request=request,
    #                   template_name='create_subtask_form.html',
    #                   context=context)

    # task_id = request.GET.get("task_id")  # getting data via query from the request, not from reverse urls
    #
    # if request == "POST":
    #     form = CreateTaskForm(request.POST)
    #
    #     if form.is_valid():
    #         form.save()
    #         return redirect("router:tasks:get-task", task_id=task_id)
    #
    # else:
    #     form = CreateSubTaskForm()
    #
    #     task = get_object_or_404(Task, id=task_id)
    #     user = get_object_or_404(User, id=request.user.id)
    #     categories = Category.objects.all()
    #     statuses = Status.objects.all()
    #
    #     context = {
    #         "form": form,
    #         "user": user,
    #         "task": task,
    #         "categories": categories,
    #         "statuses": statuses, }
    #
    #     return render(request=request,
    #                   template_name="create_subtask_form.html",
    #                   context=context)
