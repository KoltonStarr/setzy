import os
import chromadb
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

# Connect to remote ChromaDB server
chroma_client = chromadb.HttpClient(
    host=os.getenv("CHROMADB_HOST", "localhost"),
    port=int(os.getenv("CHROMADB_PORT", "8000"))
)

# Create a vector store client.
vector_store = Chroma(
    client=chroma_client,
    collection_name="sales_calls",
    embedding_function=OpenAIEmbeddings(model="text-embedding-3-large"),
)

for file in diarized_file_names:
    split_path = file.split("/")
    call_identifier = split_path[len(split_path) - 1]

    # Check if this call_identifier already exists in the vector store
    existing_docs = vector_store.get(
        where={"call_identifier": call_identifier},
        limit=1
    )
    
    if existing_docs['ids']:
        log(f"Skipping {call_identifier} - already embedded in vector store", "blue")
        continue

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