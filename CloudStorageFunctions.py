# Imports the Google Cloud client library
from google.cloud import storage

def create_storage_bucket(bucket_name):
    # Instantiates a client
    storage_client = storage.Client.from_service_account_json(
            'GCSCredentials.json')

    # The name for the new bucket
    bucket_name = bucket_name

    # Creates the new bucket
    bucket = storage_client.create_bucket(bucket_name)

    print("\nCreating bucket...")
    print('Bucket {} created.'.format(bucket.name))
    print("Done!\n")

def explicit():
    # Explicitly use service account credentials by specifying the private key
    # file.
    storage_client = storage.Client.from_service_account_json(
        'GCSCredentials.json')

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print()
    print("Bucket list: ")
    print(buckets)
    print()

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
     
    storage_client = storage.Client.from_service_account_json(
            'GCSCredentials.json')
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_stream(source_file_name)
    print("\nUploading video...")
    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))
    print("Done!\n")

"""explicit()
create_storage_bucket('my-new-videos-prueba2211-bucket-test')
explicit()"""

#upload_blob('my-new-videos-prueba2211-bucket-test', 'creating_bucket_example.mov', 'creating_bucket_example.mov')
