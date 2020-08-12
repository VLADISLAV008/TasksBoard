from rest_framework import viewsets, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin
from rest_framework.response import Response

from boards.models import Board, User, Section, Card
from boards.serializers import BoardSerializer, UserSerializer, SectionSerializer, CardSerializer
from boards.permissions import IsBoardOwnerOrBoardUserReadOnly, IsSectionUser, IsCardUser


class UserViewSet(CreateModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailViewSet(RetrieveModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(pk=user.pk)


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsBoardOwnerOrBoardUserReadOnly]

    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        user = self.request.user
        queryset = queryset.filter(owner=user)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsSectionUser]

    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        board_id = request.query_params.get('boardId', None)

        if board_id is not None:
            queryset = queryset.filter(board__id=board_id)
        else:
            queryset = queryset.none()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsCardUser]

    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        section_id = request.query_params.get('sectionId', None)

        if section_id is not None:
            queryset = queryset.filter(section__id=section_id)
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
