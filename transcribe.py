from openai import OpenAI
from dotenv import load_dotenv
import boto3
import os

load_dotenv()

# Create an S3 client
s3 = boto3.client('s3')

# Load ENV vars.
data_dir = os.getenv("DATA_DIR")
s3_bucket_name = os.getenv("S3_BUCKET_NAME")
open_api_key = os.getenv("OPENAI_API_KEY")

# Create the directories if they do not exist.
os.makedirs(data_dir, exist_ok=True)

# Instantiate open api client.
client = OpenAI(api_key=open_api_key)

# List all objects in the bucket
response = s3.list_objects_v2(Bucket=s3_bucket_name)

audio_files = []
for obj in response['Contents']:
    key = obj['Key']
    # Create the local file path
    local_file_path = os.path.join(data_dir, os.path.basename(key))
    
    if not os.path.exists(local_file_path):
        print(f"Downloading {key} to {local_file_path}...")
        s3.download_file(s3_bucket_name, key, local_file_path)
        print(f"Successfully downloaded {key}")
    else:
        print(f"{local_file_path} already exists! Skipping download...")

    audio_files.append(local_file_path)

for file in audio_files:
    print(f"Opening {file}....")
    with open(file, "rb") as audio_file:
        print("Beginning transcription of file...")
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            # model="gpt-4o-transcribe-diarize", 
            file=audio_file,
            timeout=None,
            # chunking_strategy="auto"  # Enable automatic chunking for large files.
        )

        transcript_file = f"{file}.txt"
        print(f"Transcription completed. Writing transcript to {transcript_file}")

        with open(transcript_file, 'w') as transcript_file:
            transcript_file.write(transcription.text)
        
        print("Write operation completed...")