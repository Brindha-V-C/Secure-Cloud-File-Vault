import json
import os
import time
import logging

from dotenv import load_dotenv
from azure.storage.queue import QueueClient

# Load environment variables
load_dotenv()

# ----------------------------
# Configure Logging
# ----------------------------

# Absolute path of the worker directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_FILE = os.path.join(BASE_DIR, "worker.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

# ----------------------------
# Azure Queue Client
# ----------------------------
queue = QueueClient.from_connection_string(
    conn_str=os.getenv("AZURE_STORAGE_CONNECTION_STRING"),
    queue_name=os.getenv("AZURE_QUEUE_NAME"),
)

logger.info("Worker started...")
logger.info("Waiting for messages...")

# ----------------------------
# Worker Loop
# ----------------------------
while True:

    messages = queue.receive_messages()

    found = False

    for message in messages:

        found = True

        metadata = json.loads(message.content)

        logger.info("=" * 60)
        logger.info("Processing File")
        logger.info("=" * 60)
        logger.info("File ID      : %s", metadata["file_id"])
        logger.info("Filename     : %s", metadata["filename"])
        logger.info("Blob Name    : %s", metadata["blob_name"])
        logger.info("Owner        : %s", metadata["owner"])
        logger.info("Size         : %s bytes", metadata["size"])
        logger.info("Content Type : %s", metadata["content_type"])
        logger.info("Processing Complete")
        logger.info("")

        queue.delete_message(
            message.id,
            message.pop_receipt,
        )

    if not found:
        time.sleep(3)