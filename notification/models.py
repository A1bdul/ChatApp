from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class Notification(models.Model):
    from_user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    to_user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)
