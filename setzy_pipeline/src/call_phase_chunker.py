from pydantic import BaseModel, Field
from langchain_core.documents import Document
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI
import system_prompt

# I CANNOT deterministically generate documents that represent core sections of the call. 
# -- Figure out what Sabrina's framework is for sections of the call. 
# -- Maybe include some examples of when one section ends and the other begins for shot prompting. 
# --------------------------------------------

class CallPhaseMetadata(BaseModel):
    """Metadata for a call phase."""
    phase_type: str = Field(description="Type of call phase (e.g., 'introduction', 'rapport building', 'discovery / qualification'), etc.")
    description: str = Field(description="Brief overview of the call phase.")

class CallPhase(BaseModel):
    """A single call phase with transcript text and metadata."""
    transcript_text: str = Field(description="The transcript text for this segment")
    metadata: CallPhaseMetadata = Field(description="Metadata about this segment")

class ResponseFormat(BaseModel):
    """Response schema for the LLM"""
    call_phases: list[CallPhase] = Field(description="A list of call phases")

class CallPhaseChunker:
    transcript_text: str
    call_identifier: str
    llm: Runnable

    def __init__(self, transcript_text: str, call_identifier: str):
        self.transcript_text = transcript_text
        self.call_identifier = call_identifier
        self._init_llm()

    # Initializing the LLM with structured output to ensure that it gives me a list of Documents. 
    def _init_llm(self) -> None:
        base_llm = ChatOpenAI(model="gpt-4o", temperature=0)
        self.llm = base_llm.with_structured_output(ResponseFormat)

    # I'm using an LLM call to help me chunk the audio file into call phase documents.
    def _get_raw_results(self):
        return self.llm.invoke([
            {"role": "system", "content": system_prompt.CALL_PHASE_SYSTEM_PROMPT},
            {"role": "user", "content": f"Here is the transcript:\n\n{self.transcript_text}"}
        ])
    
    # Parse the structured output of the LLM and create Document objects from each output section.
    def _parse_results_to_documents(self, raw_results) -> list[Document]:
        call_phase_documents: list[Document] = []
        for i, call_phase in enumerate(raw_results.call_phases):
            doc = Document(
                page_content=call_phase.transcript_text,
                metadata={
                    "call_identifier": self.call_identifier,
                    "type": "call_phase_chunk",
                    "total_chunks": len(raw_results.call_phases),
                    "chunk_index": i,  # Add explicit index too

                    "call_phase": call_phase.metadata.phase_type,
                    "description": call_phase.metadata.description,

                    "chunk_level": "L1",
                    "has_child_chunks": False,
                    "parent_level_identifier": "L0",
                }
            )
            call_phase_documents.append(doc)
        return call_phase_documents


    def gen_call_phase_documents(self) -> list[Document]:
        raw_results = self._get_raw_results()
        return self._parse_results_to_documents(raw_results)
