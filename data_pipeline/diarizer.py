

# This class is responsible for:
# -- Taking audio files and outputting diarized json files from them.
class AudioDiarizer:
    audio_files: list[str]

    def __init__(self, audio_files: list[str]):
        self.audio_files = audio_files

    