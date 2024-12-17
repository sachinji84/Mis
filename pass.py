import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import azure.functions as func

# Define constants
BLOB_CONTAINER_NAME = "jcr-feedbacks"

def main(resolutionInput: func.HttpRequest) -> func.HttpResponse:
    try:
        # Parse JSON body from request
        request_body = resolutionInput.get_json()
        resolution_message = request_body.get("resolution_message", "")
        message_id = request_body.get("message_id", "")

        if not resolution_message or not message_id:
            return func.HttpResponse("Invalid request body.", status_code=400)

        # Authenticate using DefaultAzureCredential (managed identity or service principal)
        credential = DefaultAzureCredential()
        blob_service_client = BlobServiceClient(
            account_url="https://<your-storage-account-name>.blob.core.windows.net",
            credential=credential
        )

        # Get Blob client
        blob_client = blob_service_client.get_blob_client(container=BLOB_CONTAINER_NAME, blob=f"{message_id}.txt")

        # Write the resolution message to a file
        blob_client.upload_blob(resolution_message, overwrite=True)

        return func.HttpResponse(f"Resolution stored successfully for message ID: {message_id}", status_code=200)

    except Exception as e:
        return func.HttpResponse(f"An error occurred: {str(e)}", status_code=500)
