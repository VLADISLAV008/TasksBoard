from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.mixins import DestroyModelMixin, RetrieveModelMixin, ListModelMixin, CreateModelMixin

from boards.models import Board, User
from boards.serializers import BoardSerializer, UserSerializer


class BoardViewSet(CreateModelMixin,
                   ListModelMixin,
                   DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class UserViewSet(ObtainAuthToken,
                  CreateModelMixin,
                  RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
