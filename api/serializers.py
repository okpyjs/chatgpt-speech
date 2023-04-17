from rest_framework import serializers


class ChatSerializer(serializers.Serializer):
    message = serializers.CharField()
    audio_model = serializers.CharField()
    # age = serializers.IntegerField()


class AudioSerializer(serializers.Serializer):
    audio_token = serializers.CharField()
