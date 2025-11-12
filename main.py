from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from transcript import Transcript
from sliding_window_chunk import gen_sliding_window_documents
from call_phase_chunk import CallPhaseChunker

# todo 
# I CANNOT deterministically generate documents for end-to-end question & answer cycles. 
# -- Introduce an agent with the sole job of generating documents for each question and answer cycle. 
# -- Include some prompting around ranting. 

# Load ENV variables.
load_dotenv()
call_identifier = "techno_guy"

transcript = Transcript("Darryl_Carter.mp3.json").write_transcript()
transcript_text = transcript.transcript_text

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

call_phase_documents = CallPhaseChunker(transcript.transcript_text, call_identifier).gen_call_phase_documents()

# embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
