from rest_framework import status
from rest_framework.views import Response, Request, APIView
from rest_framework.serializers import ValidationError

from apps.todo.models import Task  # Added
from apps.api.serializers import AllTasksSerializer  # Added


class TasksApiViews(APIView):

    def get(self, request: Request):
        tasks = Task.objects.filter(creator=request.user.id)

        if tasks:
            serializer = AllTasksSerializer(instance=tasks, many=True)

            return Response(status=status.HTTP_200_OK,
                            data=serializer.data)

        return Response(status=status.HTTP_204_NO_CONTENT,
                        data=[])

    def post(self, request: Request):
        try:
            serializer = AllTasksSerializer(data=request.data)

            serializer.is_valid(
                raise_exception=True)  # if exception, serializer.save() will not be execited. If raise_exception undefined exception will not be raise
            serializer.save()
            return Response(status=status.HTTP_201_CREATED,
                            data=serializer.data)

        except ValidationError as error:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={"error": str(error),
                                  "error_detail": error.detail,
                                  },
                            )

        # if serializer.is_valid():  # The same, but without try-except and raising exception
        #     serializer.save()
        #     return Response(status=status.HTTP_201_CREATED,
        #                     data=serializer.data)
        #
        # return Response(status=status.HTTP_400_BAD_REQUEST,
        #                 data=serializer.errors)

    def delete(self):
        pass

    def put(self):
        pass

    def patch(self):
        pass

# #################### VIA FUNCTIONS (SEE BELLOW) ######################
# from django.shortcuts import render  # Added
# from rest_framework.request import Request  # Added
# from rest_framework.response import Response  # Added
# from rest_framework import status  # Added
# from rest_framework.decorators import api_view  # Added

# from apps.api.serializers import AllTasksSerializer  # Added
# from apps.todo.models import Task  # Added
# ######################################################################


# ####### EXAMPLE VIA DEF(FUNCTIONS) USUALLY NOT USED IN PRACTICE#######

# @api_view(["GET"])  # Attention. Methods for this decorator should passed in !!!list format!!!
# def get_all_tasks_response(request: Request):  # Defined at once, that request is type Request
#     # if request.method == "GET":     # Unnecessary, because defined in decorator
#     tasks = Task.objects.all()
#
#     if tasks:
#         serializer = AllTasksSerializer(instance=tasks, many=True)  # Attention, many=True is necessarily
#         return Response(status=status.HTTP_200_OK,  # Never pass in this way: data= {"status": 200}, only as status
#                         data=serializer.data, )
#
#     return Response(status=status.HTTP_204_NO_CONTENT,
#                     data=[], )

# ####### EXAMPLE VIA DEF(FUNCTIONS) USUALLY NOT USED IN PRACTICE#######

# @api_view(["POST"])  # Attention. Methods for this decorator should passed in !!!list format!!!
# def create_new_task_response(request: Request):
#     serializer = AllTasksSerializer(data=request.data)
#
#     if serializer.is_valid():
#         serializer.save()
#
#         return Response(status=status.HTTP_201_CREATED,
#                         data=serializer.data)
#
#     return Response(status=status.HTTP_400_BAD_REQUEST,
#                     data=serializer.errors)
# ######################################################################
