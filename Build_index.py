from llama_index.core import VectorStoreIndex, Settings, SimpleDirectoryReader, StorageContext, Document
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.chroma import ChromaVectorStore

import chromadb
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()
Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

# ✅ Add function to infer source type
def infer_source_type(file_path):
    folder = os.path.basename(os.path.dirname(file_path)).lower()
    if "writing_guide" in folder:
        return "writing_guide"
    elif "my_stories" in folder:
        return "my_story"
    elif "book" in folder:
        return "book"
    else:
        return "unknown"    

def build_index():
    print("🔍 Loading documents...")
    raw_docs = SimpleDirectoryReader("data", recursive=True).load_data()
    print(f"📚 Loaded {len(raw_docs)} documents.")

    # ✅ Add metadata to documents
    documents = []
    for doc in raw_docs:
        file_path = doc.metadata.get("file_path", "")
        source_type = infer_source_type(file_path)
        doc.metadata["source_type"] = source_type
        documents.append(Document(text=doc.text, metadata=doc.metadata))

    # ✅ Chunk with sentence splitter
    splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)
    nodes = splitter.get_nodes_from_documents(documents)
    print(f"📦 Created {len(nodes)} chunks (nodes).")

    # ✅ Setup vector store
    chroma_client = chromadb.PersistentClient(path="./chroma_store")
    collection = chroma_client.get_or_create_collection("story_docs")
    vector_store = ChromaVectorStore(chroma_collection=collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # ✅ Build and persist index
    index = VectorStoreIndex(nodes, storage_context=storage_context)
    index.storage_context.persist()
    print("✅ Vector index saved to ./chroma_store")

if __name__ == "__main__":
    build_index()