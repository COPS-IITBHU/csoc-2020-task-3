from django.urls import path
from .views import *

"""
TODO:
Add the urlpatterns of the endpoints, required for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""

urlpatterns = [
    path('todo/create/', TodoCreateView.as_view()),
    path('todo/<int:pk>/', TodoDetailView.as_view()),
    path('todo/', TodoListView.as_view()),
    path('todo/<int:pk>/add-collaborators/', TodoCollab.as_view()),
    path('todo/<int:pk>/remove-collaborators/', TodoUnCollab.as_view()),
]
