import os
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Environment variables for sensitive information
storage_account_name = os.getenv('AZURE_STORAGE_ACCOUNT_NAME')
storage_account_key = os.getenv('AZURE_STORAGE_ACCOUNT_KEY')
connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

def create_container(container_name):
    """
    Create a container in Azure Blob Storage.

    :param container_name: Name of the container to create
    """
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.create_container(container_name)
        print(f"Successfully created a container: {container_name}")
    except ResourceExistsError:
        print(f"Container '{container_name}' already exists.")
    except Exception as e:
        print(f"Failed to create container: {e}")

def upload_file_to_blob(file_path, file_name, container_name):
    """
    Upload a file to Azure Blob Storage.

    :param file_path: Path to the local file
    :param file_name: Name of the file to be saved in the blob
    :param container_name: Name of the container where the file will be uploaded
    """
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

        with open(file_path, "rb") as data:
            blob_client.upload_blob(data)
        print(f"Uploaded a file with the name: {file_name} to container: {container_name}")
    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
    except ResourceNotFoundError:
        print(f"The container '{container_name}' does not exist.")
    except Exception as e:
        print(f"Failed to upload file: {e}")

def delete_blob(container_name, blob_name):
    """
    Delete a specific blob from the container.

    :param container_name: Name of the container where the blob is stored
    :param blob_name: Name of the blob to delete
    """
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_client.delete_blob()
        print(f"Deleted blob '{blob_name}' from container '{container_name}'.")
    except ResourceNotFoundError:
        print(f"The blob '{blob_name}' or container '{container_name}' does not exist.")
    except Exception as e:
        print(f"Failed to delete blob: {e}")

def delete_container(container_name):
    """
    Delete a container and all the blobs within it.

    :param container_name: Name of the container to delete
    """
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)
        container_client.delete_container()
        print(f"Deleted container '{container_name}' and all its blobs.")
    except ResourceNotFoundError:
        print(f"The container '{container_name}' does not exist.")
    except Exception as e:
        print(f"Failed to delete container: {e}")

# Usage
if __name__ == '__main__':
    container_name = 'fileholder'
    create_container(container_name)
    upload_file_to_blob('C:\\Users\\ertan\\Downloads\\beekeeper.jpg', 'beekeeperImage.jpg', container_name)
    
    # Delete the blob
    delete_blob(container_name, 'beekeeperImage.jpg')
    
    # Delete the container
    delete_container(container_name)
