import system_prompts
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from pydantic import BaseModel, Field

from transcript import Transcript
from sliding_window import gen_sliding_window_documents

# I CAN deterministically create a chunk for the entire transcript with metadata.
# WHAT metadata should I include? 
# -----------------------------------------

# I CAN deterministically generate sliding window chunks with overlaps.
# Use a langchain chunker / text-splitter to split the transcript and get the docs from it. 
# WHAT metadata should I include? 
# --------------------------------------------

# I CANNOT deterministically generate documents that represent core sections of the call. 
# -- Figure out what Sabrina's framework is for sections of the call. 
# -- Maybe include some examples of when one section ends and the other begins for shot prompting. 
# --------------------------------------------

# todo 
# I CANNOT deterministically generate documents for end-to-end question & answer cycles. 
# -- Introduce an agent with the sole job of generating documents for each question and answer cycle. 
# -- Include some prompting around ranting. 

# Load ENV variables.
load_dotenv()
call_identifier = "techno_guy"

transcript = Transcript("Darryl_Carter.mp3.json").write_transcript()
transcript_text = transcript.transcript_text

top_level_document = Document(
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

class CallPhaseMetadata(BaseModel):
    """Metadata for a call phase."""
    phase_type: str = Field(description="Type of call phase (e.g., 'introduction', 'rapport building', 'discovery / qualification'), etc.")
    description: str = Field(description="Brief overview of the call phase.")

class CallPhase(BaseModel):
    """A single call phase with transcript text and metadata."""
    transcript_text: str = Field(description="The transcript text for this segment")
    metadata: CallPhaseMetadata = Field(description="Metadata about this segment")

class ResponseFormat(BaseModel):
    """Response schema for the agent."""
    call_phases: list[CallPhase] = Field(description="A list of call phases")

# Read the transcript directly
with open("./transcripts/Darryl_Carter.txt", "r") as f:
    transcript_content = f.read()

# Use LLM with structured output directly
llm = ChatOpenAI(model="gpt-4o", temperature=0)
llm_with_structure = llm.with_structured_output(ResponseFormat)

response = llm_with_structure.invoke([
    {"role": "system", "content": system_prompts.CALL_SEGMENT_SYSTEM_PROMPT},
    {"role": "user", "content": f"Here is the transcript:\n\n{transcript_content}"}
])

call_phase_documents: list[Document] = []
for i, call_phase in enumerate(response.call_phases):
    doc = Document(
        page_content=call_phase.transcript_text,
        metadata={
            "call_identifier": call_identifier,
            "type": "call_phase_chunk",
            "total_chunks": len(response.call_phases),
            "chunk_index": i,  # Add explicit index too

            "call_phase": call_phase.metadata.phase_type,
            "description": call_phase.metadata.description,

            "chunk_level": "L1",
            "has_child_chunks": False,
            "parent_level_identifier": "L0",
        }
    )
    call_phase_documents.append(doc)




# embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
