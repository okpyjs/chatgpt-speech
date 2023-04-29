from rest_framework import serializers


class ChatSerializer(serializers.Serializer):
    user_message = serializers.CharField()
    audio_model = serializers.CharField()
    chat_model = serializers.CharField()
    system_message = serializers.CharField()
    first_chat = serializers.BooleanField()
    # age = serializers.IntegerField()


class MailVerifySerializer(serializers.Serializer):
    email = serializers.CharField()
    code = serializers.CharField()
    # age = serializers.IntegerField()


class AudioSerializer(serializers.Serializer):
    token = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    user_name = serializers.CharField()
    password = serializers.CharField()


class SignSerializer(serializers.Serializer):
    pass
