from rest_framework import serializers
from boards.models import Board, User


class BoardSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Board
        fields = ['id', 'topic', 'description', 'owner', 'created', 'users', ]


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True, )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'token', ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
