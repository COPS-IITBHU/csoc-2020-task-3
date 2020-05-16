from django.urls import path
from .views import TodoCreateView, TodoListView, TodoView, CollaboratorAddView, CollaboratorRemoveView

urlpatterns = [
    path('todo/create/', TodoCreateView.as_view()),
    path('todo/', TodoListView.as_view()),
    path('todo/<int:pk>/', TodoView.as_view()),
    path('todo/<int:pk>/add-collaborators/', CollaboratorAddView.as_view()),
    path('todo/<int:pk>/remove-collaborators/',
         CollaboratorRemoveView.as_view())
]
