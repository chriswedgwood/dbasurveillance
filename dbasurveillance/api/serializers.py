from rest_framework import serializers
from . import models


class SqlCounterSerializer(serializers.Serializer):
    value = serializers.IntegerField(source='key')
    label = serializers.CharField(source='counter')

    class Meta:
        fields = ('value', 'label')
        model = models.SqlCounter


class SqlInstanceSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField(source='key')
    label = serializers.CharField(source='instance')

    class Meta:
        fields = ('value', 'label')
        model = models.SqlInstance


