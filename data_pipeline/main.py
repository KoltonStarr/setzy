import os
import assemblyai as aai
from audio_file_manager import AudioFileManager
from diarizer import AudioDiarizer
from transcript import Transcript
from dotenv import load_dotenv
from embedder import Embedder
from logger import log
from store import VectorStore

# Load ENV vars.
load_dotenv()
data_dir = os.getenv("DATA_DIR")
transcripts_dir = os.getenv("TRANSCRIPTS_DIR")
s3_bucket_name = os.getenv("S3_BUCKET_NAME")
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

# Create the data and transcripts directories if they do not exist.
os.makedirs(data_dir, exist_ok=True)
os.makedirs(transcripts_dir, exist_ok=True)

# Instantiate a client to chromadb vector store.
vector_store = VectorStore.create_store()

log("Retrieving audio files...", "yellow")
audio_file_manager = AudioFileManager(s3_bucket_name, data_dir)
audio_file_manager.sync_audio_files()
all_audio_files = audio_file_manager.audio_files
audio_files = []
log("Finished.", "green")

# Make a list of audio files that have not yet been diarized and embedded.
# Ignore files that already exist in the vector database. 
for file in all_audio_files:
    split_file = file.split("/")
    call_identifier = f"{split_file[len(split_file) - 1]}.json"

    if not VectorStore.is_already_embedded(vector_store, call_identifier):
        audio_files.append(file)

log("Diarizing audio files...", "yellow")
audio_diarizer = AudioDiarizer(audio_files)
audio_diarizer.diarize_audio_files()
diarized_file_names = audio_diarizer.diarized_audio_files
log("Finished.", "green")

for file in diarized_file_names:
    split_path = file.split("/")
    call_identifier = split_path[len(split_path) - 1]

    log(f"Generating transcript for: {file}", "yellow")
    transcript = Transcript(file, data_dir, transcripts_dir).write_transcript()
    transcript_text = transcript.transcript_text
    log("Finished.", "green")

    embedder = Embedder(call_identifier, transcript)

    log("Generating documents...", "yellow")
    full_transcript_document = embedder.gen_full_transcript_doc()
    sliding_window_documents = embedder.gen_sliding_window_documents()
    call_phase_documents = embedder.gen_call_phase_documents()
    log("Finished.", "green")

    log("Creating and storing embeddings...", "yellow")
    all_documents = [full_transcript_document] + sliding_window_documents + call_phase_documents

    ids = vector_store.add_documents(documents=all_documents)
    log("Finished.", "green")