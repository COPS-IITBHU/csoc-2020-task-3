from django.urls import path
from .views import *

"""
TODO:
Add the urlpatterns of the endpoints, required for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""

urlpatterns = [
    path('todo/create/', TodoCreateView.as_view()),
    path('todo/',TodoView.as_view()),
    path('todo/<int:id>',SpecificTodoView.as_view()),
    path('todo/<int:id>/collaborators',CollaboratorView.as_view()),
    path('todo/edit/<int:id>',PutPatchTodoView.as_view())
]