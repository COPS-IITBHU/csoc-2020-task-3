from django.urls import path
from .views import TodoCreateView, TodoGetView, TodoDetailView

"""
TODO:
Add the urlpatterns of the endpoints, required for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""

urlpatterns = [
    path('todo/create/', TodoCreateView.as_view()),
    path('todo/', TodoGetView.as_view()),
    path('todo/<int:id>/', TodoDetailView.as_view()),

]
