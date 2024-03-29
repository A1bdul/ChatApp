import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError(_('Email account is needed'))

        if not password:
            raise ValueError(_('Email account is needed'))

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user)
        return user

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        if extra_fields.get('is_staff') is not True:
            extra_fields['is_staff'] = True

        if extra_fields.get('is_active') is not True:
            extra_fields['is_active'] = True

        if extra_fields.get('is_superuser') is not True:
            extra_fields['is_superuser'] = True

        return self.create_user(email, first_name, last_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, blank=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, unique=True, blank=True, null=True)
    password = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    contacts = models.ManyToManyField('self', symmetrical=False, related_name='contact', blank=True)
    objects = UserManager()

    REQUIRED_FIELDS = 'first_name', 'last_name'
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class ChatRoomManager(models.Manager):

    def get_or_create_room(self, u1, u2):
        is_room = ChatRoom.objects.filter(Q(user1=u1, user2=u2) | Q(user2=u1, user1=u2)).first()
        if not is_room:
            return ChatRoom.objects.create(user1=u1, user2=u2), True
        return is_room, False

    def get_connected_users(self, user):
        rooms = ChatRoom.objects.filter(Q(user1=user) | Q(user2=user))
        connected_users = []
        for room in rooms:
            conn_user = room.user1
            if conn_user == user:
                conn_user = room.user2
            connected_users.append(conn_user.id)
        return connected_users


class ChatRoom(models.Model):
    user1 = models.ForeignKey(User, null=True, blank=True, related_name='user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, blank=True, null=True, related_name='user2', on_delete=models.CASCADE)
    connected_users = models.ManyToManyField(User, related_name='connected_user')

    objects = models.Manager()
    get_room = ChatRoomManager()

    def __str__(self):
        return f'chat Room for {self.user1} and {self.user2}'

    def get_if_connected_user(self, user):
        return user in self.connected_users.all()

    class Meta:
        app_label = 'App'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, default="")

    avatar = models.ImageField(blank=True, null=True, upload_to='assets/avatars')
    cover_image = models.ImageField(blank=True, null=True, upload_to='cover_image')
    favourite = models.ManyToManyField(ChatRoom, blank=True, related_name='favourite')
    archived = models.ManyToManyField(ChatRoom, blank=True, related_name='Archived')

    def __str__(self):
        return self.user.id


class Preference(models.Model):
    chat_background = models.CharField(max_length=200)
    theme = models.CharField(max_length=20, choices=())
