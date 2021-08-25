# Generated by Django 3.2.5 on 2021-08-16 22:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_auto_20210817_0014'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='followsList',
        ),
        migrations.AddField(
            model_name='user',
            name='followsList',
            field=models.ManyToManyField(blank=True, related_name='_network_user_followsList_+', to=settings.AUTH_USER_MODEL),
        ),
    ]
