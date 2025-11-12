from pathlib import Path
import json

class TranscriptWriter:
    # Static for now.
    data_directory = "./data"
    transcripts_directory = "./transcripts"

    diarized_json_filename: str

    def __init__(self, diarized_json_filename: str):
        self.diarized_json_filename = diarized_json_filename

    # Check to ensure that the given json file exists in the data dir.
    def _file_exists(self) -> bool:
        return Path(f"{self.data_directory}/{self.diarized_json_filename}").exists()
    
    def _create_transcript(self, segments: list[dict]) -> str:
        # Mutate the format line by line.
        transcript = "\n".join(
            [f"{s['speaker']}: {s['text'].strip()}" for s in segments]
        )

        return transcript
    
    def write_transcript(self) -> None:
        # Check if file exists and throw error if it doesn't
        if not self._file_exists():
            raise FileNotFoundError("File does not exist!")
        
        # Open the diarized JSON file.
        with open(f"{self.data_directory}/{self.diarized_json_filename}") as f:
            data = json.load(f)

        # Create the newly formatted transcript.
        transcript = self._create_transcript(data["segments"])

        # Remove .json and replace with .txt
        transcript_filename = f"{self.diarized_json_filename.split(".")[0]}.txt"
        print(f"Writing {transcript_filename} to {self.transcripts_directory}")

        # Write the newly formatted transcript to the transcripts directory.
        with open(f"{self.transcripts_directory}/{transcript_filename}", 'w') as f:
            f.write(transcript)
