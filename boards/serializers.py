from rest_framework import serializers
from boards.models import Board


class BoardSerializer(serializers.HyperlinkedModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Board
        # fields = ['url', 'id', 'topic', 'description', 'owner', 'created', 'users', ]
        fields = ['url', 'id', 'topic', 'description', 'created', 'users', ]