from django.urls import include, path
from . import api_controller

urlpatterns = [
    path('checkout', api_controller.checkout),
    path('return', api_controller.return_book),
    path('overdue_books', api_controller.overdue_books)
]
