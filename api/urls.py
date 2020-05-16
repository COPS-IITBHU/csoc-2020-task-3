from django.urls import path
from .views import *

"""
TODO:
Add the urlpatterns of the endpoints, required for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""

urlpatterns = [
    path('todo/create/', TodoCreateView.as_view()),
    path('todo/', TodoListView.as_view()),
    path('todo/<int:id>/', TodoView.as_view()),
    path('todo/<int:id>/add-collaborators/', TodoAddCollaboratorsView.as_view()),
    path('todo/<int:id>/remove-collaborators/', TodoRemoveCollaboratorsView.as_view())
]