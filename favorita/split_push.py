import pandas as pd
from google.cloud import storage


def split_csv(path, column1, column2):
    df = pd.read_csv(path)

    for element1 in df[column1].unique():
        df_label1 = df[df[column1] == element1]

        for element2 in df_label1[column2].unique():
            df_label2 = df_label1[df_label1[column2] == element2]
            df_label2.to_csv(f'scratch.csv', index=False, header=True)
            upload_blob("favorita_batch1002", f'scratch.csv',
                        f'split_data/store{element1}-{element2}.csv')


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")


def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The ID of your GCS object
    # source_blob_name = "storage-object-name"

    # The path to which the file should be downloaded
    # destination_file_name = "local/path/to/file"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(
        "Downloaded storage object {} from bucket {} to local file {}.".format(
            source_blob_name, bucket_name, destination_file_name))


if __name__ == "__main__":
    # download_blob('favorita_batch1002', f'split_data/store{element1}-{element2}.csv', destination_file_name)
    pass
