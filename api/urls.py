from django.urls import path
from .views import TodoCreateView, TodoView, TodoListView, TodoAddCollaboratorView, TodoRemoveCollaboratorView

"""
TODO:
Add the urlpatterns of the endpoints, required for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""

urlpatterns = [
    path('todo/', TodoListView.as_view()),
    path('todo/create/', TodoCreateView.as_view()),
    path('todo/<int:pk>/', TodoView.as_view()),
    path('todo/<int:pk>/add-collaborators/',TodoAddCollaboratorView.as_view()),
    path('todo/<int:pk>/remove-collaborators/',TodoRemoveCollaboratorView.as_view()),
]
