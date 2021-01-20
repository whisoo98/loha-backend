from rest_framework import serializers
from .models import *


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaStream
        fields = '__all__'