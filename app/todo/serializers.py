from rest_framework import serializers
from core.models import todo_app


class TodoSerializer(serializers.ModelSerializer):
    """Serialize task"""
    class Meta:
        model = todo_app
        fields = ('id', 'titile', 'status')
        read_only_fields = ('id',)
