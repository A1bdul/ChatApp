# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer
# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# from App.models import PrivateMessage, GroupMessages
#
# channel_layer = get_channel_layer()
#
#
# @receiver([post_save], sender=PrivateMessage)
# def private_notification(sender, instance, created, *args, **kwargs):
#     print("created!!")
#     if instance.sender == instance.room.user1:
#         to_user = instance.room.user2
#     else:
#         to_user = instance.room.user1
#     count = PrivateMessage.manage.get_unread(instance.room, to_user)
#     if count <= 0:
#         count = ''
#     async_to_sync(channel_layer.group_send)(f'notification_to_{to_user.username}', {
#         'type': 'send_status', 'from': instance.sender.username,
#         'count': count
#     })
#     print("sent")
#
#
# @receiver(post_save, sender=GroupMessages)
# def group_notification(sender, instance, *args, **kwargs):
#     for member in instance.room.members.all():
#         to_user = member.participant
#         count = GroupMessages.manage.get_group_unread(instance.room, to_user)
#         if count <= 0:
#             count = ''
#         async_to_sync(channel_layer.group_send)(f'notification_to_{to_user.username}', {
#             'type': 'send_status', 'from': str(instance.room.id),
#             'count': count
#         })
