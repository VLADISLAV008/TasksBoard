from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins

from boards.models import Board
from boards.serializers import BoardSerializer


class BoardViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
