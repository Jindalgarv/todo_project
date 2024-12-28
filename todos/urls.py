from django.urls import path
from .views import TodoListCreateView, TodoDetailView, register_view, login_view, todo_list_view
from django.shortcuts import render

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('todos/', todo_list_view, name='todo-list'),
    path('todos/', TodoListCreateView.as_view(), name='todo-list-create'),
    path('todos/<int:id>/', TodoDetailView.as_view(), name='todo-detail'),
]