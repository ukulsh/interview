from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from .models import Book
from .Serializer import BookSerializer
import logging


logger = logging.getLogger(__name__)

@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def book(request):
    """API endpoints to list/create/delete/edit books"""
    if request.method == 'GET':
        try:
            limit = int(request.GET.get('limit')) if request.GET.get('limit') else 10
            offset = int(request.GET.get('offset')) if request.GET.get('offset') else 0
        except TypeError:
            return JsonResponse({'message':"limit and offset need to be integers"}, status=400)
        
        books = Book.objects.all()[offset: offset + limit]
        return JsonResponse({'books': BookSerializer(books, many=True).data, 'total_count': Book.objects.count()}, status=200)


    if request.method == 'POST':
        try:
            id = int(request.data.get('id'))
            name = request.data.get('name')
            number_of_copies = int(request.data.get('number_of_copies'))
        except TypeError:
            return JsonResponse({'message':"id and number_of_copies need to be integers"}, status=400)

        if name is None:
            return JsonResponse({'message': "name is required"}, status=400)
        try:
            book = Book.objects.get(pk=id)
            return JsonResponse({'messsage': "Book with the given id alread exists"}, status=400)
        except ObjectDoesNotExist:
            pass

        book = Book(id=id, name=name, number_of_copies=number_of_copies)
        book.save()
        return JsonResponse({'message': 'Successfully created book', 'book': BookSerializer(book).data}, status=200)


@api_view(["PUT", "DELETE"])
def book_by_id(request, id):
    """APIs to manage a given book by id"""
    if request.method == "DELETE":
        try:
            book = Book.objects.get(pk=id)
            book.delete()
            return JsonResponse({'message': 'Book successfully deleted'}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'Book with given id does not exist'}, status=404)

    if request.method == "PUT":
        name = request.data.get('name')
        try:
            number_of_copies = int(request.data.get('number_of_copies')) if request.data.get('number_of_copies') else None
        except TypeError:
            return JsonResponse({'message': 'number_of_copies needs to be integer'}, status=400)
        
        try:
            book = Book.objects.get(pk=id)
            if name:
                book.name = name
            if number_of_copies:
                book.number_of_copies = number_of_copies
            book.save()
            return JsonResponse({'message': 'Successfully updated book', 'book': BookSerializer(book).data}, status=200)    
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'Book with given id does not exist'}, status=404)
