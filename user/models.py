from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import settings
from django.db.models import Q


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError(_('Email account is needed'))

        if not username:
            raise ValueError(_('Email account is needed'))

        if not password:
            raise ValueError(_('Email account is needed'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user)
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        if extra_fields.get('is_staff') is not True:
            extra_fields['is_staff'] = True

        if extra_fields.get('is_active') is not True:
            extra_fields['is_active'] = True

        if extra_fields.get('is_superuser') is not True:
            extra_fields['is_superuser'] = True

        return self.create_user(email, username, password, **extra_fields)


class User(AbstractUser):
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, unique=True)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)

    contacts = models.ManyToManyField('self', symmetrical=False, related_name='contact', blank=True)
    objects = UserManager()

    REQUIRED_FIELDS = 'username',
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class ChatRoomManager(models.Manager):

    def get_or_create_room(self, u1, u2):
        is_room = ChatRoom.objects.filter(Q(user1=u1, user2=u2) | Q(user2=u1, user1=u2)).first()
        if not is_room:
            return ChatRoom.objects.create(user1=u1, user2=u2)
        return is_room


class ChatRoom(models.Model):
    user1 = models.ForeignKey(User, null=True, blank=True, related_name='user1', on_delete=models.SET_NULL)
    user2 = models.ForeignKey(User, blank=True, null=True, related_name='user2', on_delete=models.SET_NULL)
    connected_users = models.ManyToManyField(User, related_name='connected_user')

    objects = models.Manager()
    get_room = ChatRoomManager()

    def __str__(self):
        return f'chat Room for {self.user1} and {self.user2}'

    class Meta:
        app_label = 'App'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, default="")
    avatar = models.ImageField(blank=True, null=True, upload_to='avatars')
    cover_image = models.ImageField(blank=True, null=True, upload_to='cover_image')
    favourite = models.ManyToManyField(ChatRoom, blank=True, related_name='favourite')