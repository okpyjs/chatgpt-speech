from rest_framework import serializers


class ChatSerializer(serializers.Serializer):
    user_message = serializers.CharField()
    audio_model = serializers.CharField()
    chat_model = serializers.CharField()
    system_message = serializers.CharField()
    # age = serializers.IntegerField()


class AudioSerializer(serializers.Serializer):
    token = serializers.CharField()
