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

from django.contrib.auth.decorators import login_required


@login_required(login_url="router:user:login-existing-user")
def home_page(request):
    return render(request=request,
                  template_name="main.html",  # full way, if not defined in setting DIR
                  )


@login_required(login_url="router:user:login-existing-user")
def get_all_tasks(request):
    tasks = Task.objects.all()
    tasks_count = Task.objects.all().count()

    context = {"tasks": tasks,
               "task_count": tasks_count,
               }

    return render(request=request,
                  template_name="all_tasks.html",  # full way, if not defined in setting DIR
                  context=context)


@login_required(login_url="router:user:login-existing-user")
def create_new_task(request):
    users = User.objects.all()
    categories = Category.objects.all()
    statuses = Status.objects.all()

    form = CreateTaskForm()

    if request.method == "POST":
        form = CreateTaskForm(request.POST)

        if form.is_valid():
            task_data = form.cleaned_data
            Task.objects.create(**task_data)
            return redirect("router:tasks:get-all-tasks")

    context = {"form": form,
               "users": users,
               "categories": categories,
               "statuses": statuses, }

    return render(request=request,
                  template_name="create_task_form.html",
                  context=context)


@login_required(login_url="router:user:login-existing-user")
def update_task_by_id(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    categories = Category.objects.all()
    statuses = Status.objects.all()

    form = TaskUpdateForm(instance=task)  # instance=task parameter initializes the form with the existing task data.

    if request.method == "POST":
        form = TaskUpdateForm(request.POST,
                              instance=task)  # instance=task parameter initializes the form with the existing task data.

        if form.is_valid():
            form.save()
            return redirect("router:tasks:get-all-tasks")

    context = {"form": form,
               "task": task,
               "categories": categories,
               "statuses": statuses, }

    return render(request=request,
                  template_name="update_task_form.html",
                  context=context)


@login_required(login_url="router:user:login-existing-user")
def get_task_by_task_id(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    subtasks = SubTask.objects.filter(task=task_id)

    context = {"task": task,
               "subtasks": subtasks, }

    return render(request=request,
                  template_name="task_info.html",
                  context=context)


@login_required(login_url="router:user:login-existing-user")
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect("router:tasks:get-all-tasks")


@login_required(login_url="router:user:login-existing-user")
def get_all_subtasks_by_creator(request):
    subtasks = SubTask.objects.filter(creator=request.user, )

    context = {"subtasks": subtasks, }

    return render(request=request,
                  template_name="all_subtasks.html",
                  context=context)


@login_required(login_url="router:user:login-existing-user")
def get_subtask_by_id(request, subtask_id):
    subtask = get_object_or_404(SubTask, id=subtask_id)

    context = {"subtask": subtask, }

    return render(request=request,
                  template_name="subtask_info.html",
                  context=context)


@login_required(login_url="router:user:login-existing-user")
def update_subtask_by_subtask_id(request, subtask_id):
    subtask = get_object_or_404(SubTask, id=subtask_id)
    task_id = request.GET.get("task_id")

    categories = Category.objects.all()
    statuses = Status.objects.all()

    form = SubTaskUpdateForm(instance=subtask)

    if request.method == 'POST':
        form = SubTaskUpdateForm(request.POST, instance=subtask)

        if form.is_valid():
            form.save()
            if task_id:
                return redirect('router:tasks:get-task-by-id', task_id=task_id)
            else:
                return redirect('router:tasks:get-all-subtasks-by-creator')
                # return redirect('router:tasks:get-subtask-by-id', subtask_id=subtask_id)

    context = {"form": form,
               "subtask": subtask,
               "categories": categories,
               "statuses": statuses, }

    return render(request=request,
                  template_name='update_subtask_form.html',
                  context=context)


@login_required(login_url="router:user:login-existing-user")
def create_new_subtask(request):
    task_id = request.GET.get("task_id")

    user = get_object_or_404(User, id=request.user.id)
    task = get_object_or_404(Task, id=task_id)

    categories = Category.objects.all()
    statuses = Status.objects.all()

    form = CreateSubTaskForm()

    if request.method == 'POST':
        form = CreateSubTaskForm(request.POST)
        # form_instance = form.instance  # TEST
        # form_data = form.cleaned_data  # TEST
        if form.is_valid():
            form.save()
            return redirect('router:tasks:get-task-by-id', task_id=task_id)

    context = {"form": form,
               "user": user,
               "categories": categories,
               "statuses": statuses,
               "task": task, }

    return render(
        request=request,
        template_name='create_subtask_form.html',
        context=context)


@login_required(login_url="router:user:login-existing-user")
def delete_subtask_by_id(request, subtask_id):
    subtask = get_object_or_404(SubTask, id=subtask_id)
    task_id = request.GET.get("task_id")
    subtask.delete()

    print(task_id)
    if task_id:
        return redirect('router:tasks:get-task-by-id', task_id=task_id)
    else:
        return redirect('router:tasks:get-all-subtasks-by-creator')
