from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from transcript import Transcript
from sliding_window_chunk import gen_sliding_window_documents
from call_phase_chunk import CallPhaseChunker

from logger import log

# Load ENV variables.
load_dotenv()
# call_identifier = "techno_guy"

# log("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< BEGIN: Generate and Write Transcript >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", "yellow")
# transcript = Transcript("Darryl_Carter.mp3.json").write_transcript()
# transcript_text = transcript.transcript_text

log("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< BEGIN: Generate full_transcript and sliding_window Documents >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", "yellow")
full_transcript_document = Document(
    page_content=transcript_text, 
    metadata={
        "call_identifier": call_identifier,
        "type": "full_transcript",

        # Hierarchy markers
        "level_identifier": "L0",  # top of hierarchy
        "has_child_chunks": True
    }
)

sliding_window_documents = gen_sliding_window_documents(transcript.transcript_path, call_identifier)

log("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< BEGIN: Generate call_phase_documents >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", "yellow")
call_phase_documents = CallPhaseChunker(transcript.transcript_text, call_identifier).gen_call_phase_documents()

log("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< BEGIN: Create embeddings and Vector Store >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", "yellow")
all_documents = [full_transcript_document] + sliding_window_documents + call_phase_documents
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

vector_store = Chroma(
    collection_name="sales_calls",
    embedding_function=embeddings,
    persist_directory="./vector_store",  # Where to save data locally, remove if not necessary
)

ids = vector_store.add_documents(documents=all_documents)
log("SUCCESS: Embedding pipeline completed >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", "green")
