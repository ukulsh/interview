from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from .models import Circulation
from members.models import Member
from reservation.models import Reserve
from books.models import Book
from .Serializer import CirculationSerializer
import logging
from datetime import datetime, timedelta

@api_view(["POST", "GET"])
def checkout(request):
    if request.method == "GET":
        try:
            limit = int(request.GET.get('limit')) if request.GET.get('limit') else 10
            offset = int(request.GET.get('offset')) if request.GET.get('offset') else 0
        except TypeError:
            return JsonResponse({'message':"limit and offset need to be integers"}, status=400)
        
        circulations = Circulation.objects.filter(returned_on__isnull=True).order_by('-circulated_on')[offset: offset + limit]
        return JsonResponse({'circulations': CirculationSerializer(circulations, many=True).data, 'total_count': Circulation.objects.filter(returned_on__isnull=True).count()}, status=200)

    if request.method == "POST":
        try:
            book_id = int(request.data.get('book_id'))
            member_id = int(request.data.get('member_id'))
        except TypeError:
            return JsonResponse({'message': 'book_id and member_id need to be integers'}, status=400)
        try:
            book = Book.objects.get(pk=book_id)
            member = Member.objects.get(pk=member_id)
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'Book or Member with given id not found'}, status=404)
        
        number_of_copies_in_circulation = Circulation.objects.filter(book=book, returned_on__isnull=True).count()
        number_of_copies_reserved = Reserve.objects.filter(book=book, processed=False).count()
        if book.number_of_copies <= number_of_copies_in_circulation + number_of_copies_reserved:
            return JsonResponse({'message': 'All books are already in circulation or reserved, consider reserving the book'}, status=400)
        
        circulation = Circulation(book=book, member=member, circulated_on=datetime.utcnow())
        circulation.save()

        return JsonResponse({'message': f'Book {book.name} successfully issued to Member {member.name}', 'circulation': CirculationSerializer(circulation).data}, status=400)

@api_view(["POST", "GET"])
def return_book(request):
    if request.method == "GET":
        try:
            limit = int(request.GET.get('limit')) if request.GET.get('limit') else 10
            offset = int(request.GET.get('offset')) if request.GET.get('offset') else 0
        except TypeError:
            return JsonResponse({'message':"limit and offset need to be integers"}, status=400)
        
        books = Circulation.objects.filter(returned_on__isnull=False).order_by('-circulated_on')[offset: offset + limit]
        return JsonResponse({'books': CirculationSerializer(books, many=True).data, 'total_count': Circulation.objects.filter(returned_on__isnull=False).count()}, status=200)
    if request.method == "POST":
        try:
            book_id = int(request.data.get('book_id'))
            member_id = int(request.data.get('member_id'))
        except TypeError:
            return JsonResponse({'message': 'book_id and member_id need to be integers'}, status=400)
        try:
            book = Book.objects.get(pk=book_id)
            member = Member.objects.get(pk=member_id)
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'Book or Member with given id not found'}, status=404)

        
        circulations = Circulation.objects.filter(book=book, member=member, returned_on__isnull=True)
        if not circulations:
            return JsonResponse({'message': f'Member: {member.name} does not have Book {book.name} assigned'}, status=400)
        circulation = circulations[0]
        circulation.returned_on = datetime.utcnow()

        time_delta = (circulation.returned_on.replace(tzinfo=None) - circulation.circulated_on.replace(tzinfo=None)).days
        
        # 50 rupees per day fine
        circulation.fine_due = max(0, time_delta - 7) * 50
        
        circulation.save()
        return JsonResponse({'message': f'Book {book.name} has been successfully returned by member {member.name} for a fine of {circulation.fine_due}', 'circulation': CirculationSerializer(circulation).data}, status=200)

@api_view(["GET"])
def overdue_books(request):
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    circulations = Circulation.objects.filter(returned_on__isnull=True, circulated_on__lt=seven_days_ago)
    total_fines_due = 0
    today_date = datetime.utcnow()
    for circulation in circulations:
        days_overdue =  (today_date - circulation.circulated_on.replace(tzinfo=None)).days
        fine_due = max(0, days_overdue - 7) * 50
        circulation.fine_due = fine_due
        circulation.save()
        total_fines_due += circulation.fine_due
    
    return JsonResponse({'total_fine_due': total_fines_due, 'circulations_overdue': CirculationSerializer(circulations, many=True).data}, status=200)
