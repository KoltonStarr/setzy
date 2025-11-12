from pathlib import Path
import json

class Transcript:
    # Static for now.
    data_directory = "./data"
    transcripts_directory = "./transcripts"

    diarized_json_filename: str

    _transcript_text: str
    _transcript_path: str

    def __init__(self, diarized_json_filename: str):
        self.diarized_json_filename = diarized_json_filename
        self._create_transcript()
        self._set_transcript_path()

    # Check to ensure that the given json file exists in the data dir.
    def _file_exists(self) -> bool:
        return Path(f"{self.data_directory}/{self.diarized_json_filename}").exists()
    
    # Sets the path for the transcript.
    def _set_transcript_path(self) -> None:
        transcript_filename = f"{self.diarized_json_filename.split(".")[0]}.txt"
        self._transcript_path = f"{self.transcripts_directory}/{transcript_filename}"
    
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
    
    @property
    def transcript_path(self):
        """Getter for transcript text"""
        return self._transcript_path
    
    def write_transcript(self):
        # Write the newly formatted transcript to the transcripts directory.
        with open(self._transcript_path, 'w') as f:
            f.write(self._transcript_text)

        print("Successfully wrote transcript to transcripts directory!")
        
        return self
