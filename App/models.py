import uuid
from django.db import models
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
            if user not in message.read.all():
                message.read.add(user)
                message.save()

    def read_group_message(self, room, user):
        messages = GroupMessages.objects.filter(room=room)
        for message in messages:
            if user not in message.read.all():
                message.read.add(user)
                message.save()

    def get_unread(self, room, user):
        x = PrivateMessage.objects.filter(room=room)
        count = 0
        for message in x:
            if user not in message.read.all():
                count += 1
        return count

    def get_group_unread(self, room, user):
        x = GroupMessages.objects.filter(room=room)
        count = 0
        for message in x:
            if user not in message.read.all():
                count += 1
        return count


class Album(models.Model):
    """ upload images to the cloudinary storage and storing the url in database"""
    images = models.URLField()

    def __str__(self):
        return self.images


class Folder(models.Model):
    """ upload files to the cloudinary storage and storing the url in database"""
    files = models.URLField()


class DefaultMessages(BaseModel):
    """ Basis of all message model regardless of weather group or private room"""
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.SET_NULL, null=True)
    msg = models.TextField(blank=True, null=True)
    reply = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.SET_NULL)
    images = models.ManyToManyField(Album, blank=True, related_name='has_image')
    files = models.ManyToManyField(Folder, blank=True, related_name="has_files")
    read = models.ManyToManyField(User, default=sender)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super(DefaultMessages, self).save()
        self.read.add(self.sender)

class Member(models.Model):
    """ Model for the members in the group chat, the is_admin attribute handles
        if member can do certain function to group
    """
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)


class Group(BaseModel):
    """
        Group Chat models
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    icon = models.ImageField(blank=True, null=True)
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(Member, blank=False)


class GroupMessages(DefaultMessages):
    """
        Deriving from default messages and assigning to the already
        created a group chat
    """
    room = models.ForeignKey(Group, on_delete=models.CASCADE)

    objects = models.Manager()
    manage = MessageManager()

    class Meta:
        verbose_name = 'group message'
        verbose_name_plural = 'group messages'


class PrivateMessage(DefaultMessages):
    """
        Deriving from default messages and assigning to the already
        created a private chat room
    """
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)

    objects = models.Manager()
    manage = MessageManager()

    def __str__(self):
        return f'message from {self.sender}, {self.id}'
    