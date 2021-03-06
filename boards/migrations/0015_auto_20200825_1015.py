# Generated by Django 3.0.8 on 2020-08-25 07:15

from django.db import migrations, models
import django.utils.crypto


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0014_auto_20200818_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='token',
            field=models.CharField(default=django.utils.crypto.get_random_string, max_length=30, unique=True),
        ),
    ]
