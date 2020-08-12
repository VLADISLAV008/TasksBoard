from rest_framework import viewsets, permissions, generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.mixins import DestroyModelMixin, RetrieveModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.response import Response

from boards.models import Board, User, Section
from boards.serializers import BoardSerializer, UserSerializer, SectionSerializer


class UserViewSet(CreateModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailViewSet(RetrieveModelMixin,
                        viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(owner=user)


class SectionViewSet(viewsets.ModelViewSet):
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Section.objects.filter(board__owner=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        board_id = request.query_params.get('boardId', None)

        if board_id is not None:
            queryset = queryset.filter(board__id=board_id)
        else:
            queryset = queryset.none()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'userId': user.pk,
        })
