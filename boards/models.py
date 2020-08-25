from django.db import models

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.crypto import get_random_string
from rest_framework.authtoken.models import Token

from boards.managers.UserManager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(db_index=True, max_length=255, unique=True)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('password',)

    objects = UserManager()

    @property
    def token(self):
        return Token.objects.get_or_create(user=self)[0]


class Board(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, related_name='owner_board_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=30, unique=True, default=get_random_string)
    users = models.ManyToManyField(User, blank=True, related_name='guest_board_set')

    class Meta:
        ordering = ['created']


class Section(models.Model):
    board = models.ForeignKey(Board, related_name='section_set', on_delete=models.CASCADE)
    topic = models.CharField(max_length=100)
    description = models.TextField(blank=True)


class Card(models.Model):
    section = models.ForeignKey(Section, related_name='card_set', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    performer = models.ForeignKey(User, null=True, blank=True, related_name='performing_card_set',
                                  on_delete=models.SET_NULL)
