from django.shortcuts import render

from apps.todo.models import Task  # Added


# Create your views here.


def home_page(request):
    return render(request=request,
                  template_name="todo/main.html")


def get_all_tasks(request):
    tasks = Task.objects.all()
    context = {"tasks": tasks, }
    return render(request=request,
                  template_name="todo/all_tasks.html",
                  context=context)
