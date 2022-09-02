import uuid

from django.db import models
from django.db.models import Q
from user.models import User, ChatRoom


# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class MessageManager(models.Manager):
    def get_queryset(self, **kwargs):
        room = kwargs['room']
        return super(MessageManager, self).get_queryset().filter(room=room).all()

    def read_all_message(self, room, user):
        messages = PrivateMessage.objects.filter(room=room)
        for message in messages:
            message.read.add(user)
            message.save()


class Album(models.Model):
    images = models.URLField()

    def __str__(self):
        return self.images


class Folder(models.Model):
    files = models.URLField()


class DefaultMessages(BaseModel):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.SET_NULL, null=True)
    msg = models.TextField(blank=True, null=True)
    reply = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.SET_NULL)
    images = models.ManyToManyField(Album, blank=True, related_name='has_image')
    files = models.ManyToManyField(Folder, blank=True, related_name="has_files")


class Member(models.Model):
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)


class Group(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    icon = models.ImageField(blank=True, null=True)
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(Member, blank=False)


class GroupMessages(DefaultMessages):
    room = models.ForeignKey(Group, on_delete=models.CASCADE)
    read_by = models.ManyToManyField(Member)

    objects = models.Manager()
    manage = MessageManager()

    class Meta:
        verbose_name = 'group message'
        verbose_name_plural = 'group messages'


class PrivateMessage(DefaultMessages):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    read = models.ManyToManyField(User)

    objects = models.Manager()
    manage = MessageManager()

    def __str__(self):
        return f'message from {self.sender}, {self.id}'
