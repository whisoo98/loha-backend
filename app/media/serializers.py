from rest_framework import serializers

from .models import *


class MediaSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = MediaStream
        fields = '__all__'

    def get_thumbnail(self, media):
        asset_playback_id = media.mux_asset_playback_id
        live_playback_id = media.mux_livestream_playback_id

        if asset_playback_id:
            playback_id = asset_playback_id
        else:
            playback_id = live_playback_id

        url = f"https://image.mux.com/{playback_id}/thumbnail.png"
        return url


class MediaSerializerforClient(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = MediaStream
        exclude = ['mux_livestream_id', 'mux_asset_id', 'updated_at', 'finished_at', 'product_list']

    def get_thumbnail(self, media):
        asset_playback_id = media.mux_asset_playback_id
        live_playback_id = media.mux_livestream_playback_id

        if asset_playback_id:
            playback_id = asset_playback_id
        else:
            playback_id = live_playback_id

        url = f"https://image.mux.com/{playback_id}/thumbnail.png"
        return url
