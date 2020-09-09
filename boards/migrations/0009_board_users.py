# Generated by Django 3.0.8 on 2020-08-12 08:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0008_auto_20200810_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='available_board_set', to=settings.AUTH_USER_MODEL),
        ),
    ]