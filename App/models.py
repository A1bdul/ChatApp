from django.db import models
from django.db.models import Q
from user.models import User


# Create your models here.
class ChatRoomManager(models.Manager):

    def get_or_create_room(self, u1, u2):
        is_room = ChatRoom.objects.filter(Q(user1=u1, user2=u2) | Q(user2=u1, user1=u2)).first()
        if not is_room:
            return ChatRoom.objects.create(user1=u1, user2=u2)
        return is_room


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class ChatRoom(BaseModel):
    user1 = models.ForeignKey(User, null=True, blank=True, related_name='user1', on_delete=models.SET_NULL)
    user2 = models.ForeignKey(User, blank=True, null=True, related_name='user2', on_delete=models.SET_NULL)

    objects = models.Manager()
    get_room = ChatRoomManager()

    def __str__(self):
        return f'chat Room for {self.user1} and {self.user2}'


class MessageManager(models.Manager):
    def by_room(self, room):
        messages = Messages.objects.filter(room=room).order_by('created_at').all()
        return messages


class Album(models.Model):
    images = models.URLField()

    def __str__(self):
        return self.images


class Folder(models.Model):
    files = models.URLField()


class Messages(BaseModel):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    msg = models.TextField(blank=True, null=True)
    reply = models.ForeignKey('Messages', null=True, blank=True, related_name='replies', on_delete=models.SET_NULL)
    images = models.ManyToManyField(Album, blank=True, related_name='has_image')
    files = models.ManyToManyField(Folder, blank=True, related_name="has_files")
    read = models.BooleanField(default=True)

    objects = models.Manager()
    manage = MessageManager()

class Members(models.Model):
    participant = models.ForeignKey(User, on_delete=models.CASCADE)

