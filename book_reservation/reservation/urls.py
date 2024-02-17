from django.urls import include, path
from . import api_controller

urlpatterns = [
    path('', api_controller.reserve),
    path('fulfill', api_controller.fulfill)
]
