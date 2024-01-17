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
    task_id = request.GET.get("task_id")
    if not task_id:
        print(task_id)
        raise ValueError("Invalid task ID")

    user = get_object_or_404(User, id=request.user.id)
    if not user:
        print(user)
        raise ValueError(f"Invalid user ID")

    task = get_object_or_404(Task, id=task_id)
    if not task:
        print(task)
        raise ValueError(f"Invalid task ID")

    categories = Category.objects.all()
    statuses = Status.objects.all()

    form = CreateSubTaskForm()

    # error_messages = form.errors
    # # cleaned_data = form.cleaned_data
    # data = form.data
    # fields = form.fields
    # instance = form.instance
    # base_fields = form.base_fields

    if request.method == 'POST':
        form = CreateSubTaskForm(request.POST)
        if form.is_valid():
            print("cleaned_data:", form.cleaned_data)

            form.save()
            return redirect('router:tasks:get-task-by-id', task_id=task_id)

    error_messages = form.errors
    # cleaned_data = form.cleaned_data
    data = form.data
    fields = form.fields
    instance = form.instance
    base_fields = form.base_fields
    # value = form.value

    for error in error_messages:
        print("error:", error)
    print("data:", data)
    # print("cleaned data:", cleaned_data)
    print("fields:", fields)
    print("instance:", instance)
    print("base_fields:", base_fields)
    # print("value:", value)

    context = {
        "form": form,
        "user": user,
        "categories": categories,
        "statuses": statuses,
        "task": task,
        "error_messages": error_messages,
    }

    return render(
        request=request,
        template_name='create_subtask_form.html',
        context=context
    )

    # task_id = request.GET.get("task_id")
    #
    # if request.method == 'POST':
    #     form = CreateSubTaskForm(request.POST)
    #
    #     if form.is_valid():
    #         form.save()
    #         return redirect('router:tasks:get-task-by-id', task_id=task_id)
    #
    # user = get_object_or_404(User, id=request.user.id)
    # task = get_object_or_404(Task, id=task_id)
    # categories = Category.objects.all()
    # statuses = Status.objects.all()
    #
    # form = CreateSubTaskForm()
    #
    # context = {"form": form,
    #            "user": user,
    #            "categories": categories,
    #            "statuses": statuses,
    #            "task": task
    #            }
    #
    # return render(request=request,
    #               template_name='create_subtask_form.html',
    #               context=context)


def delete_subtask_by_id(request, subtask_id):
    subtask = get_object_or_404(SubTask, id=subtask_id)
    task_id = request.GET.get("task_id")

    subtask.delete()
    return redirect('router:tasks:get-task-by-id', task_id=task_id)
