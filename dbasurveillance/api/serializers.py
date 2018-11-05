from rest_framework import serializers
from . import models


class SqlCounterSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('key', 'instance')
        model = models.SqlCounter
