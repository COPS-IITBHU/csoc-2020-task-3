from django.urls import path,include
from .views import TodoCreateView,TodoListView,TodoDetailView
from .collaborations import AddCollaboration,RemoveCollaboration

"""
TODO:
Add the urlpatterns of the endpoints, required for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""

urlpatterns = [
    path('todo/create/', TodoCreateView.as_view(),name="create-view"),
    path('todo/',TodoListView.as_view(),name="list-view"),
    path('todo/<int:id>/',TodoDetailView.as_view(),name="detail-view"),
    path('todo/<int:id>/add-collaboration/<str:user>/',AddCollaboration.as_view(),name="add"),
    path('todo/<int:id>/remove-collaboration/<str:user>/',RemoveCollaboration.as_view(),name="remove")
]

