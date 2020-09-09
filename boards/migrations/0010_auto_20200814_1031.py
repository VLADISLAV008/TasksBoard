# Generated by Django 3.0.8 on 2020-08-14 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0009_board_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='card_set', to='boards.Section'),
        ),
    ]