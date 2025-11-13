import os
from openai import OpenAI
from audio_file_manager import AudioFileManager
from dotenv import load_dotenv

# Load ENV vars.
load_dotenv()
data_dir = os.getenv("DATA_DIR")
s3_bucket_name = os.getenv("S3_BUCKET_NAME")
open_api_key = os.getenv("OPENAI_API_KEY")

# Create the directories if they do not exist.
os.makedirs(data_dir, exist_ok=True)
os.makedirs("./transcipts", exist_ok=True)

audio_file_manager = AudioFileManager(s3_bucket_name, data_dir)
audio_file_manager.sync_audio_files()
audio_files = audio_file_manager.audio_files

# Instantiate open api client.
client = OpenAI(api_key=open_api_key)

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