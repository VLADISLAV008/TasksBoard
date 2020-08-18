from django.db.models import Q
from rest_framework import viewsets, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin
from rest_framework.response import Response

from boards.models import User, Section, Card, Board
from boards.serializers import BoardSerializer, UserSerializer, SectionSerializer, CardSerializer
from boards.permissions import IsSectionUser, IsCardUser, IsBoardOwner, IsBoardGuestReadOnly


class UserViewSet(CreateModelMixin, RetrieveModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return User.objects.none()
        return User.objects.all()


class BoardViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,
                          IsBoardOwner | IsBoardGuestReadOnly]

    def get_serializer_class(self):
        if self.action == 'users':
            return UserSerializer
        return BoardSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = user.owner_board_set.all() | user.guest_board_set.all()
        return queryset.distinct()

    def perform_create(self, serializer):
        token = Board.generate_token(12)
        serializer.save(token=token)

    @action(detail=True)
    def users(self, request, pk=None):
        queryset = User.objects.all()
        board = self.get_object()
        if board is not None:
            queryset = board.users
        else:
            queryset = queryset.none()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def invite_link(self, request):
        user = request.user
        board = Board.objects.all().filter(token=request.data['token'])[0]

        if (board is not None) and (user != board.owner) and (user not in board.users.all()):
            board.users.add(user)
            board.save()
        serializer = self.get_serializer(board, many=False)
        return Response(serializer.data)


class SectionViewSet(viewsets.ModelViewSet):
    serializer_class = SectionSerializer
    filterset_fields = ['board']
    permission_classes = [permissions.IsAuthenticated,
                          IsSectionUser]

    def get_queryset(self):
        user = self.request.user
        queryset = Section.objects.all()
        queryset = queryset.filter(Q(board__owner=user) | Q(board__users__pk=user.pk))
        return queryset.distinct()


class CardViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    filterset_fields = ['section']
    permission_classes = [permissions.IsAuthenticated,
                          IsCardUser]

    def get_queryset(self):
        user = self.request.user
        queryset = Card.objects.all()
        queryset = queryset.filter(Q(section__board__owner=user) | Q(section__board__users__pk=user.pk))
        return queryset.distinct()

    def update(self, request, *args, **kwargs):
        card = self.get_object()
        new_section = Section.objects.all().filter(pk=request.data['section'])[0]
        if card.section.board.pk != new_section.board.pk:
            return Response({'detail': 'permission denied'}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
        })
