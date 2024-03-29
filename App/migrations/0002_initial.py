# Generated by Django 4.2.5 on 2023-10-01 19:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='group',
            name='connected_users',
            field=models.ManyToManyField(related_name='connected_members', to='App.member'),
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(to='App.member'),
        ),
        migrations.AddField(
            model_name='defaultmessages',
            name='files',
            field=models.ManyToManyField(blank=True, related_name='has_files', to='App.folder'),
        ),
        migrations.AddField(
            model_name='defaultmessages',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='has_image', to='App.album'),
        ),
        migrations.AddField(
            model_name='defaultmessages',
            name='read',
            field=models.ManyToManyField(default=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sender', to=settings.AUTH_USER_MODEL), to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='defaultmessages',
            name='reply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='replies', to='App.defaultmessages'),
        ),
        migrations.AddField(
            model_name='defaultmessages',
            name='sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sender', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chatroom',
            name='connected_users',
            field=models.ManyToManyField(related_name='connected_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chatroom',
            name='user1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chatroom',
            name='user2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user2', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='privatemessage',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.chatroom'),
        ),
        migrations.AddField(
            model_name='groupmessages',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.group'),
        ),
    ]
