from django.urls import include, path
from . import api_controller

urlpatterns = [
    path('', api_controller.member),
    path('<int:id>', api_controller.member_by_id)
]
