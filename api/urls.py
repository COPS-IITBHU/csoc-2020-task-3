from django.urls import path
from .views import *

"""
TODO:
Add the urlpatterns of the endpoints, required for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""

urlpatterns = [
    path('todo/', TodoListView.as_view()),
    path('todo/create/', TodoCreateView.as_view()),
    path('todo/<int:pk>/', TodoOpsView.as_view()),
    path('users/', UserList.as_view()),
    path('todo/<int:pk>/add-collaborators/', CollaboratorAddView.as_view()),
    path('todo/<int:pk>/remove-collaborators/', CollaboratorRemoveView.as_view())
]