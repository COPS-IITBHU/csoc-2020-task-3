from django.urls import path,include
from .views import TodoCreateView,TodoListView,TodoDetailView

"""
TODO:
Add the urlpatterns of the endpoints, required for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""

urlpatterns = [
    path('todo/create/', TodoCreateView.as_view(),name="create-view"),
    path('todo/',TodoListView.as_view(),name="list-view"),
    path('todo/<int:id>/',TodoDetailView.as_view(),name="detail-view")
]

