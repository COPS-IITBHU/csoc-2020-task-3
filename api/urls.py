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
    path('todo/<int:id>/collaborators',collaboratorsView.as_view())
]