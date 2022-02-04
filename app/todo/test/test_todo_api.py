from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import todo_app
from todo.serializers import TodoSerializer

TODO_URL = reverse('todo:todo-list')


def sample_task(user, **params):
    """Create and return a sample task"""
    defaults = {
        'titile': 'Read a book at 8 PM',
        'status': 'Yet to be completed',
    }
    defaults.update(params)

    return todo_app.objects.create(user=user, **defaults)


class PublicTodoApiTests(TestCase):
    """Test unauthenticated todo api access"""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """Test that authentication is required"""
        res = self.client.get(TODO_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTodoAPITests(TestCase):
    """Test unauthenticated todo api access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='riti23455@gmail.com',
            password='Riti@12345'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_tasks(self):
        """Test that retrieving a list of tasks"""
        sample_task(user=self.user)
        sample_task(user=self.user)

        res = self.client.get(TODO_URL)
        tasks = todo_app.objects.all().order_by('-id')
        serializer = TodoSerializer(tasks, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_task_limited_to_user(self):
        """Test retrieving tasks for user"""
        user2 = get_user_model().objects.create_user(
            email='riti22334@gmail.com',
            password='Riar#2233'
        )
        sample_task(user=user2)
        sample_task(user=self.user)

        res = self.client.get(TODO_URL)

        tasks = todo_app.objects.filter(user=self.user)
        serializer = TodoSerializer(tasks, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)
