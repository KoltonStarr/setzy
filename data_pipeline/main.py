import os
import assemblyai as aai
from audio_file_manager import AudioFileManager
from diarizer import AudioDiarizer
from dotenv import load_dotenv

# Load ENV vars.
load_dotenv()
data_dir = os.getenv("DATA_DIR")
s3_bucket_name = os.getenv("S3_BUCKET_NAME")
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

# Create the directories if they do not exist.
os.makedirs(data_dir, exist_ok=True)
os.makedirs("./transcipts", exist_ok=True)

audio_file_manager = AudioFileManager(s3_bucket_name, data_dir)
audio_file_manager.sync_audio_files()
audio_files = audio_file_manager.audio_files

audio_diarizer = AudioDiarizer(audio_files)
audio_diarizer.diarize_audio_files()