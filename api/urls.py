from django.urls import path
from .views import TodoCreateView, TodoViewSet, CollaboratorViewSet

"""
TODO:
Add the urlpatterns of the endpoints, required for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'^todo', TodoViewSet)
router.register(r'^todo', CollaboratorViewSet)

urlpatterns = [
    path('todo/create/', TodoCreateView.as_view()),
]
urlpatterns+=router.urls