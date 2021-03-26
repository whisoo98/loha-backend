from rest_framework import serializers
from .models import *


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaStream
        fields = '__all__'


class MediaSerializerforClient(serializers.ModelSerializer):
    class Meta:
        model = MediaStream
        exclude = ['mux_livestream_id', 'mux_asset_id', 'updated_at', 'finished_at', 'product_list']
