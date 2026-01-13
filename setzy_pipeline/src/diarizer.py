import assemblyai as aai
from assemblyai import Transcript
import os
import json

# This class is responsible for:
# -- Taking audio files and outputting diarized json files from them.
class AudioDiarizer:
    _audio_files: list[str] = []
    _diarized_audio_files: list[str] = []
    _config: aai.TranscriptionConfig

    @property
    def diarized_audio_files(self) -> list[str]:
        return self._diarized_audio_files

    def __init__(self, audio_files: list[str]):
        self._audio_files = audio_files
        self._init_config()

    # Initialize AssemblyAI Configuration.
    def _init_config(self) -> None:
        self._config = aai.TranscriptionConfig(
            speech_model=aai.SpeechModel.universal,
            speaker_labels=True,
            speakers_expected=2,
            disfluencies=True
        )

    # 
    def _generate_transcript(self, audio_file: str) -> Transcript:
        transcript = aai.Transcriber(config=self._config).transcribe(audio_file)
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
        for file in self._audio_files:
            print(f"Beginning diarization of {file}")
            diarized_file_name = f"{file}.json"
            self.diarized_audio_files.append(diarized_file_name)

            # If the diarized file already exists then skip.
            if os.path.exists(diarized_file_name):
                print(f"{diarized_file_name} already exists!")
                continue

            with open(file, "rb") as audio_file:
                transcript = self._generate_transcript(audio_file)
                diarized_data = self._generate_diarized_json(transcript)
                with open(diarized_file_name, 'w') as f:
                    json.dump(diarized_data, f, indent=2)

                print(f"{diarized_file_name} CREATED.")



