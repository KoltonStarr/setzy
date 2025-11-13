import os
import json
import assemblyai as aai
from audio_file_manager import AudioFileManager
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

# Enable speaker diarization
config = aai.TranscriptionConfig(
    speech_model=aai.SpeechModel.universal,
    speaker_labels=True,
    speakers_expected=2
)

for file in audio_files:
    print(f"Opening {file}....")
    with open(file, "rb") as audio_file:
        print("Beginning transcription of file...")

        transcript = aai.Transcriber(config=config).transcribe(audio_file)
        if transcript.status == "error":
            raise RuntimeError(f"Transcription failed: {transcript.error}")
        print("Transcription completed.")

        # Create diarized JSON with speaker labels
        diarized_data = {
            "segments": [
                {
                    "speaker": utterance.speaker,
                    "text": utterance.text,
                    "start": utterance.start,
                    "end": utterance.end,
                    "confidence": utterance.confidence
                }
                for utterance in transcript.utterances
            ],
            "full_text": transcript.text
        }

        diarized_file_name = f"{file}.json"
        with open(diarized_file_name, 'w') as f:
            json.dump(diarized_data, f, indent=2)
        
        print("Write operation completed...")