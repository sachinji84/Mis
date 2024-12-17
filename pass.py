import os
import azure.functions as func
from azure.storage.blob import BlobServiceClient

# Load configuration from environment variables
BLOB_CONNECTION_STRING = os.environ["BLOB_STORAGE_CONNECTION_STRING"]
BLOB_CONTAINER_NAME = "jcr-feedbacks"

def main(resolutionInput: func.HttpRequest) -> func.HttpResponse:
    try:
        # Parse JSON body from request
        request_body = resolutionInput.get_json()
        resolution_message = request_body.get("resolution_message", "")
        message_id = request_body.get("message_id", "")

        if not resolution_message or not message_id:
            return func.HttpResponse("Invalid request body.", status_code=400)

        # Connect to Azure Blob Storage
        blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=BLOB_CONTAINER_NAME, blob=f"{message_id}.txt")

        # Write the resolution message to a file
        with blob_client.upload_blob(resolution_message, overwrite=True) as blob:
            return func.HttpResponse(f"Resolution stored successfully for message ID: {message_id}", status_code=200)

    except Exception as e:
        return func.HttpResponse(f"An error occurred: {str(e)}", status_code=500)
