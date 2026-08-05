from azure.storage.blob import BlobServiceClient
from django.conf import settings
import uuid


class AzureBlobService:

    def __init__(self):
        self.blob_service_client = BlobServiceClient.from_connection_string(
            settings.AZURE_STORAGE_CONNECTION_STRING
        )

        self.container_client = self.blob_service_client.get_container_client(
            settings.AZURE_CONTAINER_NAME
        )

    def upload_file(self, uploaded_file):
        """
        Upload a file to Azure Blob Storage.

        Returns:
            blob_name
            blob_url
        """

        extension = uploaded_file.name.split(".")[-1]

        blob_name = f"uploads/{uuid.uuid4()}.{extension}"

        blob_client = self.container_client.get_blob_client(blob_name)

        blob_client.upload_blob(
            uploaded_file,
            overwrite=True,
            content_type=uploaded_file.content_type,
        )

        return blob_name, blob_client.url
    

    def download_blob(self, blob_name):

        blob_client = self.container_client.get_blob_client(blob_name)

        return blob_client.download_blob().readall()
    

    def delete_blob(self, blob_name):
        blob_client = self.container_client.get_blob_client(blob_name)
        blob_client.delete_blob()