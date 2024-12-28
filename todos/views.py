from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Todo
from .serializers import TodoSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class TodoListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        todos = Todo.objects.filter(user=request.user)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TodoDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            todo = Todo.objects.get(id=id, user=request.user)
            serializer = TodoSerializer(todo)
            return Response(serializer.data)
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            todo = Todo.objects.get(id=id, user=request.user)
            serializer = TodoSerializer(todo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            todo = Todo.objects.get(id=id, user=request.user)
            todo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'error': 'Missing username or password'}, status=400)
    user = User.objects.create_user(username=username, password=password)
    refresh = RefreshToken.for_user(user)
    return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})

@api_view(['POST'])
def login(request):
    # Token-based login handled automatically by SimpleJWT
    pass  # Refer to DRF documentation

def register_view(request):
    return render(request, 'todos/register.html')

def login_view(request):
    return render(request, 'todos/login.html')

def todo_list_view(request):
    return render(request, 'todos/todo_list.html')