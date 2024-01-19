# #################### VIA FUNCTIONS ###################################
# CONTENT:
# def get_all_tasks_response
# def create_new_task_response

from django.shortcuts import render  # Added
from rest_framework.request import Request  # Added
from rest_framework.response import Response  # Added
from rest_framework import status  # Added
from rest_framework.decorators import api_view  # Added

from apps.api.serializers import AllTasksSerializer  # Added
from apps.todo.models import Task  # Added


# ##### VIEWS VIA FUNCTIONS (SAMPLES) USUALLY NOT USED IN PRACTICE #####

@api_view(["GET"])  # Attention. Methods for this decorator should passed in !!!list format!!!
def get_all_tasks_response(request: Request):  # Defined at once, that request is type Request
    # if request.method == "GET":     # Unnecessary, because defined in decorator
    tasks = Task.objects.all()

    if tasks:
        serializer = AllTasksSerializer(instance=tasks, many=True)  # Attention, many=True is necessarily
        return Response(status=status.HTTP_200_OK,  # Never pass in this way: data= {"status": 200}, only as status
                        data=serializer.data, )

    return Response(status=status.HTTP_204_NO_CONTENT,
                    data=[], )


@api_view(["POST"])  # Attention. Methods for this decorator should passed in !!!list format!!!
def create_new_task_response(request: Request):
    serializer = AllTasksSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=serializer.data)

    return Response(status=status.HTTP_400_BAD_REQUEST,
                    data=serializer.errors)
