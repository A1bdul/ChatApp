from django.db import models
from django.contrib.auth import get_user_model

from App.models import Group


class NotificationManager(models.Manager):
    def seen_count(self, group, user):
        x = Notification.objects.filter(group=group)
        count = 0
        for notifys in x:
            if user not in notifys.user_has_seen.all():
                count += 1
        return count

    def has_seen_all(self, group, user):
        x = Notification.objects.filter(group=group)
        for notifys in x:
            notifys.user_has_seen.add(user)
            notifys.save()

# Create your models here.
class Notification(models.Model):
    from_user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='from_user')
    to_user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='to_user')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, related_name='group')
    user_has_seen = models.ManyToManyField(get_user_model(), default=from_user)
    date = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    notify = NotificationManager()

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save()
        self.user_has_seen.add(self.from_user)
