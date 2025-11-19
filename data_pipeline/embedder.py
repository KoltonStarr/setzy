from transcript import Transcript
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from call_phase_chunker import CallPhaseChunker

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200, 
    chunk_overlap=70, 
    add_start_index=True, 
    length_function=len
)

class Embedder:
    _call_identifier: str
    _transcript: Transcript

    def __init__(self, call_identifier: str, transcript: Transcript) -> Document:
        self ._call_identifier = call_identifier
        self._transcript = transcript

    # Generates a single document of the entire transcript.
    def gen_full_transcript_doc(self):
        transcript_text = self._transcript.transcript_text
        call_identifier = self._call_identifier

        return Document(
            page_content=transcript_text, 
            metadata={
                "call_identifier": call_identifier,
                "type": "full_transcript",

                # Hierarchy markers
                "level_identifier": "L0",  # top of hierarchy
                "has_child_chunks": True
            }
        )
    
    # Generates fixed chunk documents with slight character overlap.
    def gen_sliding_window_documents(self) -> list[Document]:
        transcript_filepath = self._transcript.transcript_filepath
        call_identifier = self._call_identifier

        raw_chunks = TextLoader(transcript_filepath).load()
        sliding_window_documents = text_splitter.split_documents(raw_chunks)

        for i, document in enumerate(sliding_window_documents):
            document.metadata.update({
                "call_identifier": call_identifier,
                "type": "sliding_window_chunk",
                "total_chunks": len(sliding_window_documents),
                "chunk_index": i,  # Add explicit index too

                "chunk_level": "L2",
                "has_child_chunks": False,
                "parent_level_identifier": "L0",
                "description": "Fixed chunk not split at any clear call boundary."
            })
        
        return sliding_window_documents

    # Generates smart call phase documents.
    def gen_call_phase_documents(self) -> list[Document]:
        transcript_text = self._transcript.transcript_text
        call_identifier = self._call_identifier

        return CallPhaseChunker(transcript_text, call_identifier).gen_call_phase_documents()
