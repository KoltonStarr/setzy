from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

# I CAN deterministically generate sliding window chunks with overlaps.
# Use a langchain chunker / text-splitter to split the transcript and get the docs from it. 
# WHAT metadata should I include? 
# --------------------------------------------

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200, 
    chunk_overlap=70, 
    add_start_index=True, 
    length_function=len
)

def gen_sliding_window_documents(transcript_path: str, call_identifier: str) -> list[Document]:
    raw_chunks = TextLoader(transcript_path).load()
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