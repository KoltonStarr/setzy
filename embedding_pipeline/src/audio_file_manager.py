import boto3
import os

# This class is responsible for:
# -- Pulling audio files from an S3 bucket. 
# -- Writing the audio files to a local data directory. 
# -- Maintaining a list of those files and making them available to other callers. 
class AudioFileManager:
    s3_client: any
    s3_bucket: str 
    data_dir: str

    # A list of absolute filepaths.
    _audio_files: list[str] = []

    def __init__(self, s3_bucket: str, data_dir: str):
        self.s3_bucket = s3_bucket
        self.data_dir = data_dir

        # Create an S3 client
        self.s3_client = boto3.client('s3')

    @property
    def audio_files(self) -> list[str]:
        return self._audio_files

    def sync_audio_files(self) -> None:
        s3 = self.s3_client
        s3_bucket_name = self.s3_bucket
        data_dir = self.data_dir
        # Get a list of all the object keys in the bucket.
        response = s3.list_objects_v2(Bucket=s3_bucket_name)
        for obj in response['Contents']:
            key = obj['Key']

            # Create the file in the data_dir where the filename is the key of the object from S3.
            local_file_path = os.path.join(data_dir, os.path.basename(key))
            
            # Only download file data if it does not exist in the data directory.
            if not os.path.exists(local_file_path):
                print(f"Downloading {key} to {local_file_path}...")
                s3.download_file(s3_bucket_name, key, local_file_path)
                print(f"Successfully downloaded {key}")
            else:
                print(f"{local_file_path} already exists! Skipping download...")

            self._audio_files.append(local_file_path)
