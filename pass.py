import azure.functions as func
import os
import requests
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Parse the incoming JSON payload from SharePoint
        req_body = req.get_json()
        resolution_data = req_body.get('Resolution')

        if not resolution_data:
            return func.HttpResponse("No resolution data provided.", status_code=400)

        # Azure Storage Configuration
        connection_string = os.getenv('AzureWebJobsStorage')
        blob_container_name = "jcr-container"  # Replace with your container name

        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=blob_container_name, blob="resolution-data.txt")

        # Upload resolution data to Blob Storage
        blob_client.upload_blob(resolution_data, overwrite=True)

        return func.HttpResponse("Resolution data uploaded successfully.", status_code=200)

    except Exception as e:
        return func.HttpResponse(f"Error occurred: {str(e)}", status_code=500)
