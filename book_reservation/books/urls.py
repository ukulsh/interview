from django.urls import include, path
from . import api_controller

urlpatterns = [
    path('', api_controller.book),
    path('<int:id>', api_controller.book_by_id)
]
