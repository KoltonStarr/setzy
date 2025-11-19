import os
import assemblyai as aai
from audio_file_manager import AudioFileManager
from diarizer import AudioDiarizer
from transcript import Transcript
from dotenv import load_dotenv
from embedder import Embedder
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from logger import log

# Load ENV vars.
load_dotenv()
data_dir = os.getenv("DATA_DIR")
transcripts_dir = os.getenv("TRANSCRIPTS_DIR")
s3_bucket_name = os.getenv("S3_BUCKET_NAME")
persist_directory = os.getenv("VECTOR_STORE_PERSIST_DIRECTORY")
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

# Create the directories if they do not exist.
os.makedirs(data_dir, exist_ok=True)
os.makedirs(transcripts_dir, exist_ok=True)

log("Getting audio files...", "yellow")
audio_file_manager = AudioFileManager(s3_bucket_name, data_dir)
audio_file_manager.sync_audio_files()
audio_files = audio_file_manager.audio_files
log("Finished.", "green")


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
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    vector_store = Chroma(
        collection_name="sales_calls",
        embedding_function=embeddings,
        persist_directory=persist_directory,  # Where to save data locally, remove if not necessary
    )

    ids = vector_store.add_documents(documents=all_documents)
    log("Finished.", "green")
