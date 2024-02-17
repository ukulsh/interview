from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from .models import Member
from .Serializer import MemberSerializer
import logging


logger = logging.getLogger(__name__)

@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def member(request):
    """API endpoints to list/create/delete/edit members"""
    if request.method == 'GET':
        try:
            limit = int(request.GET.get('limit')) if request.GET.get('limit') else 10
            offset = int(request.GET.get('offset')) if request.GET.get('offset') else 0
        except TypeError:
            return JsonResponse({'message':"limit and offset need to be integers"}, status=400)
        
        members = Member.objects.all()[offset: offset + limit]
        return JsonResponse({'members': MemberSerializer(members, many=True).data, 'total_count': Member.objects.count()}, status=200)


    if request.method == 'POST':
        try:
            id = int(request.data.get('id'))
            name = request.data.get('name')
        except TypeError:
            return JsonResponse({'message':"id need to be integers"}, status=400)

        if name is None:
            return JsonResponse({'message': "name is required"}, status=400)
        try:
            member = Member.objects.get(pk=id)
            return JsonResponse({'messsage': "Member with the given id alread exists"}, status=400)
        except ObjectDoesNotExist:
            pass

        member = Member(id=id, name=name)
        member.save()
        return JsonResponse({'message': 'Successfully created member', 'member': MemberSerializer(member).data}, status=200)


@api_view(["PUT", "DELETE"])
def member_by_id(request, id):
    """APIs to manage a given member by id"""
    if request.method == "DELETE":
        try:
            member = Member.objects.get(pk=id)
            member.delete()
            return JsonResponse({'message': 'Member successfully deleted'}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'Member with given id does not exist'}, status=404)

    if request.method == "PUT":
        name = request.data.get('name')    
        try:
            member = Member.objects.get(pk=id)
            if name:
                member.name = name
            member.save()
            return JsonResponse({'message': 'Successfully updated member', 'member': MemberSerializer(member).data}, status=200)    
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'Member with given id does not exist'}, status=404)
