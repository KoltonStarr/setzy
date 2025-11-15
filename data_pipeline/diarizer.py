import assemblyai as aai
from assemblyai import Transcript
import json

# This class is responsible for:
# -- Taking audio files and outputting diarized json files from them.
class AudioDiarizer:
    audio_files: list[str]
    config: aai.TranscriptionConfig

    def __init__(self, audio_files: list[str]):
        self.audio_files = audio_files
        self._init_config()

    # Initialize AssemblyAI Configuration.
    def _init_config(self) -> None:
        self.config = aai.TranscriptionConfig(
            speech_model=aai.SpeechModel.universal,
            speaker_labels=True,
            speakers_expected=2,
            disfluencies=True
        )

    # 
    def _generate_transcript(self, audio_file: str) -> Transcript:
        transcript = aai.Transcriber(config=self.config).transcribe(audio_file)
        if transcript.status == "error":
            raise RuntimeError(f"Transcription failed: {transcript.error}")
        print("Transcription completed.")

        return transcript
    
    def _generate_diarized_json(self, transcript: Transcript) -> dict[str, any]:
        return {
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

    def diarize_audio_files(self) -> None:
        for file in self.audio_files:
            with open(file, "rb") as audio_file:
                print(f"Beginning diarization of {file}")

                transcript = self._generate_transcript(audio_file)
                diarized_data = self._generate_diarized_json(transcript)

                diarized_file_name = f"{file}.json"
                with open(diarized_file_name, 'w') as f:
                    json.dump(diarized_data, f, indent=2)

                print(f"{diarized_file_name} CREATED.")



