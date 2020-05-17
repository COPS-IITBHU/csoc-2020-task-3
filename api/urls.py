from django.urls import path
from .views import TodoCreateView,TodoGetView,TodoDetailedView,CollabTodo,AddCollaborator,DeleteCollaborator,CollabTodoDetailedView,TodoCollaboratorsListView

"""
TODO:
Add the urlpatterns of the endpoints, required for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""

urlpatterns = [
    path('todo/create/', TodoCreateView.as_view()),
    path('todo/get/', TodoGetView.as_view()),
    path('todo/<int:id>/', TodoDetailedView.as_view()),
    path('collab/todo/get/', CollabTodo.as_view()),
    path('todo/<int:id>/list-collaborators/', TodoCollaboratorsListView.as_view()),
    path('todo/<int:id>/add-collaborator/', AddCollaborator.as_view()),
    path('todo/<int:id>/delete-collaborator/', DeleteCollaborator.as_view()),
    path('collab/todo/<int:id>/', CollabTodoDetailedView.as_view()),
]