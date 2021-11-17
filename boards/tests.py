from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from boards.models import User, Board


def create_user(username, password, first_name, last_name):
    return User.objects.create(username=username, password=password, first_name=first_name, last_name=last_name)


def create_board(title, description, owner, users):
    time = timezone.now()
    board = Board.objects.create(title=title, description=description, owner=owner, created=time)
    for user in users:
        board.users.add(user)
    return board

class BoardViewSetTests(APITestCase):
    def test_create_board_by_authenticated_user(self):
        create_user('user', 'password', 'Elon', 'Musk')
        user = User.objects.get(username='user')
        self.client.force_authenticate(user=user)

        url = reverse('board-list')
        data = {'title': 'Title', 'description': 'Description'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Board.objects.count(), 1)
        self.assertEqual(Board.objects.get().title, 'Title')
        self.assertEqual(Board.objects.get().description, 'Description')
        self.assertEqual(Board.objects.get().owner.pk, user.pk)
        self.assertEqual(len(Board.objects.get().token), 13)

    def test_create_board_by_not_authenticated_user(self):
        url = reverse('board-list')
        data = {'title': 'Title', 'description': 'Description'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_absence_other_user_board_in_list_boards_by_owner(self):
        user = create_user('user', 'password', 'Elon', 'Musk')
        user2 = create_user('user2', 'password', 'Elon', 'Musk')
        create_board('Board 1', 'Description', user2, [])

        self.client.force_authenticate(user=user)
        url = reverse('board-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_boards_by_owner(self):
        user = create_user('user', 'password', 'Elon', 'Musk')
        user2 = create_user('user2', 'password', 'Elon', 'Musk')

        create_board('Board 1', 'Description', user2, [user])
        create_board('Board 2', '', user, [])

        self.client.force_authenticate(user=user)
        url = reverse('board-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_board_by_participant(self):
        user = create_user('user', 'password', 'Elon', 'Musk')
        user2 = create_user('user2', 'password', 'Elon', 'Musk')

        board = create_board('Board 1', 'Description', user2, [user])

        self.client.force_authenticate(user=user)
        url = reverse('board-detail', kwargs={'pk': board.id})
        data = {'title': 'New Title', 'description': 'New Description'}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_board_by_owner(self):
        user = create_user('user', 'password', 'Elon', 'Musk')
        board = create_board('Board 1', 'Description', user, [])

        self.client.force_authenticate(user=user)
        url = reverse('board-detail', kwargs={'pk': board.id})
        data = {'title': 'New Title', 'description': 'New Description'}
        response = self.client.put(url, data, format='json')

        updated_board = Board.objects.get(pk=board.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_board.title, 'New Title')
        self.assertEqual(updated_board.description, 'New Description')

    def test_get_participants_list_by_participant(self):
        user = create_user('user', 'password', 'Elon', 'Musk')
        user2 = create_user('user2', 'password', 'Elon', 'Musk')

        board = create_board('Board 1', 'Description', user2, [user])

        self.client.force_authenticate(user=user)
        url = reverse('board-users', kwargs={'pk': board.id})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_participants_list_by_owner(self):
        user = create_user('user', 'password', 'Elon', 'Musk')
        user2 = create_user('user2', 'password', 'Elon', 'Musk')

        board = create_board('Board 1', 'Description', user, [user2])

        self.client.force_authenticate(user=user)
        url = reverse('board-users', kwargs={'pk': board.id})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_invite_link_list_by_owner(self):
        user = create_user('user', 'password', 'Elon', 'Musk')

        board = create_board('Board 1', 'Description', user, [])

        self.client.force_authenticate(user=user)
        url = reverse('board-get-invite-link', kwargs={'pk': board.id})
        response = self.client.get(url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['token']), 12)

    def test_get_invite_link_by_participant(self):
        user = create_user('user', 'password', 'Elon', 'Musk')
        user2 = create_user('user2', 'password', 'Elon', 'Musk')

        board = create_board('Board 1', 'Description', user2, [user])

        self.client.force_authenticate(user=user)
        url = reverse('board-get-invite-link', kwargs={'pk': board.id})
        response = self.client.get(url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
