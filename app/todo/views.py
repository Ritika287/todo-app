from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from todo import serializers
from core.models import todo_app


class TodoViewSet(viewsets.ModelViewSet):
    """Manage tasts in the db"""
    serializer_class = serializers.TodoSerializer
    queryset = todo_app.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


def get_queryset(self):
    """Retrieve tasks for authenticated user"""
    return self.queryset.filter(user=self.request.user)
