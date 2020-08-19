from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from boards.models import User, Board, Section


def create_user(username, password, first_name, last_name):
    return User.objects.create(username=username, password=password, first_name=first_name, last_name=last_name)


def create_board(title, description, owner, users):
    time = timezone.now()
    token = Board.generate_token(12)
    board = Board.objects.create(title=title, description=description, owner=owner, created=time, token=token)
    for user in users:
        board.users.add(user)
    return board


def create_section(board, topic, description):
    return Section.objects.create(board=board, topic=topic, description=description)


class BoardViewSetTests(APITestCase):
    def test_create_board_by_authenticated_user(self):
        create_user('user', 'password', 'Elon', 'Musk')
        user = User.objects.get(username='user')
        self.client.force_authenticate(user=user)

        url = reverse('board-list')
        data = {'title': 'Title', 'description': 'Description', 'owner': user.pk}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Board.objects.count(), 1)
        self.assertEqual(Board.objects.get().title, 'Title')
        self.assertEqual(Board.objects.get().description, 'Description')
        self.assertEqual(Board.objects.get().owner.pk, user.pk)
        self.assertEqual(len(Board.objects.get().token), 12)

    def test_create_board_by_not_authenticated_user(self):
        user = create_user('user', 'password', 'Elon', 'Musk')

        url = reverse('board-list')
        data = {'title': 'Title', 'description': 'Description', 'owner': user.pk}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_empty_list_boards_by_owner(self):
        user = create_user('user', 'password', 'Elon', 'Musk')
        user2 = create_user('user2', 'password', 'Elon', 'Musk')
        self.client.force_authenticate(user=user)

        create_board('Board 1', 'Description', user2, [])

        url = reverse('board-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_boards_by_owner(self):
        create_user('user', 'password', 'Elon', 'Musk')
        user = User.objects.get(username='user')
        self.client.force_authenticate(user=user)

        create_board('Board 1', '', user, [])

        url = reverse('board-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class SectionViewSetTests(APITestCase):
    def test_list_sections_by_board_id_by_owner(self):
        create_user('user', 'password', 'Elon', 'Musk')
        user = User.objects.get(username='user')
        self.client.force_authenticate(user=user)

        board_1 = create_board('Board 1', '', user, [])
        create_section(board_1, 'Section 1', '')
        create_section(board_1, 'Section 2', '')

        board_2 = create_board('Board 2', '', user, [])
        create_section(board_2, 'Section 1', '')

        url = reverse('section-list')
        response = self.client.get(url, {'board': board_1.pk}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Section.objects.count(), 3)
        self.assertEqual(len(response.data), 2)

    def test_list_sections_by_owner(self):
        user_1 = create_user('user', 'password', 'Elon', 'Musk')
        user_2 = create_user('user2', 'password', 'Elon', 'Musk')
        self.client.force_authenticate(user=user_1)

        board_1 = create_board('Board 1', '', user_1, [])
        create_section(board_1, 'Section 1', '')
        create_section(board_1, 'Section 2', '')

        board_2 = create_board('Board 2', '', user_1, [])
        create_section(board_2, 'Section 1', '')

        board_3 = create_board('Board 3', '', user_2, [])
        create_section(board_3, 'Section 1', '')

        url = reverse('section-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Board.objects.count(), 3)
        self.assertEqual(Section.objects.count(), 4)
        self.assertEqual(len(response.data), 3)
