from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import settings


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
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        if extra_fields.get('is_staff') is not True:
            extra_fields['is_staff'] = True

        if extra_fields.get('is_active') is not True:
            extra_fields['is_active'] = True

        if extra_fields.get('is_superuser') is not True:
            extra_fields['is_superuser'] = True

        return self.create_user(email, username, password, **extra_fields)


class ContactList(models.Model):
    name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    favourite = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class BlackList(models.Model):
    name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class User(AbstractUser):
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, unique=True)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    bio = models.TextField(blank=True, default="")
    avatar = models.ImageField(blank=True, null=True, upload_to='avatars')
    cover_image = models.ImageField(blank=True, null=True, upload_to='cover_image')
    contacts = models.ManyToManyField(ContactList, blank=True)
    block_list = models.ManyToManyField(BlackList, blank=True)
    about = models.TextField(blank=True)

    objects = UserManager()

    REQUIRED_FIELDS = 'username',
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
