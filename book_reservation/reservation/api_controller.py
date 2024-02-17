from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from .models import Reserve
from members.models import Member
from books.models import Book
from circulation.models import Circulation
from circulation.Serializer import CirculationSerializer
from .Serializer import ReserveSerializer
import logging
from datetime import datetime


@api_view(["GET", "POST", "DELETE"])
def reserve(request):
    if request.method == "GET":
        try:
            limit = int(request.GET.get('limit')) if request.GET.get('limit') else 10
            offset = int(request.GET.get('offset')) if request.GET.get('offset') else 0
        except TypeError:
            return JsonResponse({'message':"limit and offset need to be integers"}, status=400)
        
        reservations = Reserve.objects.filter().order_by('-reserved_on')[offset: offset + limit]
        return JsonResponse({'reservations': ReserveSerializer(reservations, many=True).data, 'total_count': Reserve.objects.filter().count()}, status=200)

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
        if book.number_of_copies > number_of_copies_in_circulation:
            return JsonResponse({'message': 'Books are available in circulation, proceed to direct checkout'}, status=400)
        
        reserve = Reserve(book=book, member=member, reserved_on=datetime.utcnow())
        reserve.save()
        return JsonResponse({'message': f'Successfully reserved Book {book.name} for Member {member.name}', 'reservation':ReserveSerializer(reserve).data}, status=200)

    if request.method == "DELETE":
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
        
        reservation = Reserve.objects.filter(book=book, member=member, processed=False)
        if not reservation:
            return JsonResponse({'message': f'No reservation found for Member: {member.name} with book {book.name}'}, status=404)
        
        reservation = reservation[0]
        reservation.delete()
        return JsonResponse({'message': 'Reservation successfully deleted', 'reservation': ReserveSerializer(reservation).data}, status=200)

@api_view(["POST"])
def fulfill(request):
    if request.data.get('book_id') is None:
        return JsonResponse({'message': 'please provide book_id'}, status=400)
    book_id = int(request.data.get('book_id'))
    try:
        book = Book.objects.get(pk=book_id)
    except ObjectDoesNotExist:
        return JsonResponse({'message': 'Book with given id not found'}, status=404)
    
    reservations = Reserve.objects.filter(book=book, processed=False).order_by('reserved_on')
    if not reservations:
        return JsonResponse({'message': 'No reservations to process'}, status=400)
    
    reservation =reservations[0]
    
    if reservation.processed:
        return JsonResponse({'message': 'Reservation was already processed'}, status=400)
    number_of_copies_in_circulation = Circulation.objects.filter(book=reservation.book, returned_on__isnull=True).count()
    if reservation.book.number_of_copies <= number_of_copies_in_circulation:
        return JsonResponse({'message': 'Books are not available in circulation, try again later'}, status=400)
        
    reservation.processed = True
    circulation = Circulation(book=reservation.book, member=reservation.member, circulated_on=datetime.utcnow())
    circulation.save()
    reservation.save()

    return JsonResponse({'message': 'Reservation request successfully fulfilled', 'reservation': ReserveSerializer(reservation).data, 'circulation': CirculationSerializer(circulation).data}, status=200)