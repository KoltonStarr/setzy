import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import os
import assemblyai as aai
from audio_file_manager import AudioFileManager
from diarizer import AudioDiarizer
from transcript import Transcript
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
diarized_file_names = audio_diarizer.diarized_audio_files

for file in enumerate(diarized_file_names):
    split_path = file.split("/")
    call_identifier = split_path[len(split_path) - 1]

    transcript = Transcript(file).write_transcript()
    transcript_text = transcript.transcript_text