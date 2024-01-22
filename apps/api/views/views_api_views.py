# #################### Via ApiViews Classes ############################
# CONTENT:
# class TasksApiViews(APIView) with GET, POST

from rest_framework import status  # Added
from rest_framework.views import Response, Request, APIView  # Added
from rest_framework.serializers import ValidationError

from apps.todo.models import Task  # Added
from apps.api.serializers import TaskModelSerializer  # Added


# ############### VIEWS VIA API VIEWS CLASSES (SAMPLES) ################
class TasksApiViews(APIView):

    def get(self, request: Request):
        tasks = Task.objects.filter(creator=request.user.id)

        if tasks:  # if tasks.exists() the same result
            serializer = TaskModelSerializer(instance=tasks, many=True)
            return Response(status=status.HTTP_200_OK,
                            data=serializer.data)

        return Response(status=status.HTTP_204_NO_CONTENT,
                        data=[])

    def post(self, request: Request):
        serializer = TaskModelSerializer(data=request.data)

        if serializer.is_valid():  # The same, but without try-except and raising exception (see bellow)
            serializer.save()
            return Response(status=status.HTTP_201_CREATED,
                            data=serializer.data)

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data=serializer.errors)

        # The same result (validation and posting option 2)
        # try:
        #     serializer = AllTasksSerializer(data=request.data)
        #
        #     serializer.is_valid(
        #         raise_exception=True)  # if except, .save() will not be executed
        #     serializer.save()
        #     return Response(status=status.HTTP_201_CREATED,
        #                     data=serializer.data)
        #
        # except ValidationError as error:
        #     return Response(status=status.HTTP_400_BAD_REQUEST,
        #                     data={"error": str(error),
        #                           "error_detail": error.detail}, )

    # def delete(self):
    #     pass

    # def put(self):
    #     pass

    # def patch(self):
    #     pass
