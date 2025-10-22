from django.contrib.auth.models import User
from rest_framework.generics import (
    ListCreateAPIView,
      RetrieveUpdateDestroyAPIView
)
from rest_framework import status
from rest_framework.response import Response

from api.serializers import UserSerializer

class UserListCreateView(ListCreateAPIView):
    """ 
     GET /api/users/ - List all users
     POST /api/users/ - Create a new user
     returns a list of users or creates a new user.
     """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """ 
     GET /api/users/{pk}/ - Retrieve a user
     PUT /api/users/{pk}/ - Update a user
     PATCH /api/users/{pk}/ - Partially update a user
     DELETE /api/users/{pk}/ - Delete a user
     returns, updates, or deletes a specific user by primary key.
     """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_destroy(self, instance):
        if instance.is_active:
            instance.is_active = False
            instance.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "detail":f'user {instance.username} deactivated'
            },
            status=status.HTTP_200_OK
        )
