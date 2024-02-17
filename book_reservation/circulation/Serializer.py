from rest_framework import serializers
from .models import Circulation

class CirculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circulation
        fields = "__all__"
