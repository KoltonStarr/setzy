from pathlib import Path
import json

class Transcript:
    # Static for now.
    data_directory = "./data"
    transcripts_directory = "./transcripts"

    diarized_json_filename: str

    _transcript_text: str

    def __init__(self, diarized_json_filename: str):
        self.diarized_json_filename = diarized_json_filename
        self._create_transcript()

    # Check to ensure that the given json file exists in the data dir.
    def _file_exists(self) -> bool:
        return Path(f"{self.data_directory}/{self.diarized_json_filename}").exists()
    
    def _create_transcript(self) -> str:
        # Check if json file exists and throw error if it doesn't.
        if not self._file_exists():
            raise FileNotFoundError("File does not exist! Unable to create transcript.")
        
        # Open the diarized JSON file.
        with open(f"{self.data_directory}/{self.diarized_json_filename}") as f:
            data = json.load(f)
        
        # Mutate the format line by line.
        transcript_text = "\n".join(
            [f"{s['speaker']}: {s['text'].strip()}" for s in data["segments"]]
        )

        self._transcript_text = transcript_text
    
    @property
    def transcript_text(self):
        """Getter for transcript text"""
        return self._transcript_text
    
    def write_transcript(self):
        # Remove .json and replace with .txt
        transcript_filename = f"{self.diarized_json_filename.split(".")[0]}.txt"
        print(f"Writing {transcript_filename} to {self.transcripts_directory}")

        # Write the newly formatted transcript to the transcripts directory.
        with open(f"{self.transcripts_directory}/{transcript_filename}", 'w') as f:
            f.write(self._transcript_text)

        print("Successfully wrote transcript to transcripts directory!")
        
        return self
