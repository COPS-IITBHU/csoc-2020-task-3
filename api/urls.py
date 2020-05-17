from django.urls import path
from . import views

"""
TODO:
Add the urlpatterns of the endpoints, required for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""

urlpatterns = [
    path('todo/create/', views.TodoCreateView.as_view()),
    path('todo/', views.ListTodo.as_view()),
    path('todo/<int:id>/', views.DetailTodo.as_view()),
    path('todo/<int:id>/add-collaborators/',views.TodoAddCollaborator.as_view()),
    path('todo/<int:id>/remove-collaborators/',views.TodoRemoveCollaborator.as_view()),
]