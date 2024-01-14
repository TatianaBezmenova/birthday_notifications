import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from notifications.consts import BASE_NOTIFICATION, NO_BIRTHDAY_MESSAGE
from notifications.models import Employee
from notifications.serializers import custom_serialize
from notifications.views import get_birthday_data


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = BASE_NOTIFICATION

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def send_message(self, event):
        message = event['message']
        self.send(text_data=message)

    @receiver([post_save, post_delete], sender=Employee)
    def handle_database_change(sender, instance, **kwargs):
        """Отправляет новое уведомление, если в таблице сотрудников произошли изменения."""
        birthday_data = get_birthday_data()
        message = '' if birthday_data else NO_BIRTHDAY_MESSAGE

        birthday_data = custom_serialize(birthday_data)
        json_data = json.dumps({
            'data': birthday_data,
            'message': message,
        })

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(BASE_NOTIFICATION, {
            'type': 'send_message',
            'message': json_data,
        })
