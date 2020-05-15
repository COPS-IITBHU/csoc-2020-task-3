from django.urls import path
from .views import TodoCreateView,TodoListView,TodoDetailView,ColloboratorAdd,ColloboratorRemove


"""
TODO:
Add the urlpatterns of the endpoints, required for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""

urlpatterns = [
    path('todo/create/', TodoCreateView.as_view()),
    path('todo/', TodoListView.as_view()),
    path('todo/<int:id>/',TodoDetailView.as_view()),
    path('todo/<int:id>/add-collaborators/',ColloboratorAdd.as_view()),
    path('todo/<int:id>/remove-collaborators/<int:coid>/',ColloboratorRemove.as_view())
]