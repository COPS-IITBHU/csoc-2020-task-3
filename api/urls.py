from django.urls import path
from .views import TodoCreateView, TodoListView, TodoView

urlpatterns = [
    path('todo/create/', TodoCreateView.as_view()),
    path('todo/', TodoListView.as_view()),
    path('todo/<int:pk>/', TodoView.as_view())
]
