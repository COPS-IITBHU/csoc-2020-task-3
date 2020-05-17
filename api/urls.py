from django.urls import path
from .views import *

"""
TODO:
Add the urlpatterns of the endpoints, required for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""

urlpatterns = [
    path('todo/create/', TodoCreateView.as_view()),
    path('todo/',TodoListView.as_view()),
    path('todo/<int:id>/',TodoDetailView.as_view()),
    path('todo/<int:id>/add-collaborators/',AddCollaborator.as_view()),
    path('todo/<int:id>/remove-collaborators/',RemoveCollaborator.as_view())
]