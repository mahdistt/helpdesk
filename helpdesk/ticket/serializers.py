from rest_framework import serializers

from . import models


class QuerySerializer(serializers.ModelSerializer):
    """
         Serializer class form Organization
    """

    class Meta:
        model = models.Query
        fields = (
            'subject',
            'message',
            'status',
            'is_active',
            'create_info',
            'slug',
            'user_related',
            'category_related',
        )


class ReplaySerializer(serializers.ModelSerializer):
    """
         Serializer class form Organization
    """

    class Meta:
        model = models.Replay
        fields = (
            'replay_message',
            'create_info',
            'query_related',
            'operator_related',

        )
