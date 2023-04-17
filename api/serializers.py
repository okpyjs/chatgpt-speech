from rest_framework import serializers


class ChatSerializer(serializers.Serializer):
    message = serializers.CharField()
    # age = serializers.IntegerField()
