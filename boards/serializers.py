from rest_framework import serializers
from boards.models import Board, User, Section, Card


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title', 'description', 'owner', 'users', 'token']
        read_only_fields = ('owner', 'token')


class InviteActivateSerializer(serializers.Serializer):
    token = serializers.SlugRelatedField(slug_field='token', queryset=Board.objects.all())


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id', 'topic', 'description', 'board']


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'name', 'description', 'section', 'performer']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True, )

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
