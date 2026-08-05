import json

from azure.storage.queue import QueueClient
from django.conf import settings


class AzureQueueService:

    def __init__(self):
        self.queue = QueueClient.from_connection_string(
            conn_str=settings.AZURE_STORAGE_CONNECTION_STRING,
            queue_name=settings.AZURE_QUEUE_NAME,
        )

    def send_message(self, metadata):

        self.queue.send_message(
            json.dumps(metadata)
        )