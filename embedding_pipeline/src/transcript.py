from pathlib import Path
import json

class Transcript:
    # Static for now.
    data_dir: str
    transcripts_dir: str

    diarized_json_filepath: str

    _transcript_text: str
    _transcript_filepath: str

    def __init__(self, diarized_json_filepath: str, data_dir: str, transcripts_dir: str):
        self.diarized_json_filepath = diarized_json_filepath
        self.data_dir = data_dir 
        self.transcripts_dir = transcripts_dir

        self._create_transcript()
        self._set_transcript_filepath()

    # Check to ensure that the given json file exists in the data dir.
    def _file_exists(self) -> bool:
        return Path(f"{self.diarized_json_filepath}").exists()
    
    # Sets the path for the transcript.
    def _set_transcript_filepath(self) -> None:
        split_path = self.diarized_json_filepath.split("/")
        transcript_filename = f"{split_path[len(split_path) - 1].split(".")[0]}.txt"

        self._transcript_filepath = f"{self.transcripts_dir}/{transcript_filename}"
    
    def _create_transcript(self) -> str:
        # Check if json file exists and throw error if it doesn't.
        if not self._file_exists():
            raise FileNotFoundError("File does not exist! Unable to create transcript.")
        
        # Open the diarized JSON file.
        with open(f"{self.diarized_json_filepath}") as f:
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
    def transcript_filepath(self):
        """Getter for transcript text"""
        return self._transcript_filepath
    
    def write_transcript(self):
        # Write the newly formatted transcript to the transcripts directory.
        with open(self._transcript_filepath, 'w') as f:
            f.write(self._transcript_text)

        print("Successfully wrote transcript to transcripts directory!")
        
        return self
