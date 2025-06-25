import streamlit as st
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.together import TogetherLLM
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from dotenv import load_dotenv
import chromadb
import os

# Load environment variables
load_dotenv()

# Set up embedding and LLM
Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

Settings.llm = TogetherLLM(
    api_key=os.getenv("TOGETHER_API_KEY"),
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    temperature=0.7,
    max_tokens=512
)

# Custom system prompt
custom_prompt = """
You are a personalized creative writing assistant.

- Use 'my_story' documents to understand the user’s writing style: tone, genre, and feel.
- Use 'writing_guide' documents to help improve story grammar, flow, pacing, and technique.
- Use 'book' documents for inspiration, plot techniques, and character ideas, but do not copy or mimic them.

Be supportive, creative, and align suggestions to the user’s personal voice unless guided otherwise.
"""

# Load Chroma and index
@st.cache_resource(show_spinner="Loading vector index...")
def load_query_engine():
    chroma_client = chromadb.PersistentClient(path="./chroma_store")
    collection = chroma_client.get_or_create_collection("story_docs")
    vector_store = ChromaVectorStore(chroma_collection=collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)
    
    return index.as_query_engine(
        similarity_top_k=5,
        system_prompt=custom_prompt
    )

query_engine = load_query_engine()

# Streamlit App Layout
st.title("📝 StoryMentor - AI Writing Assistant")
st.markdown("Ask questions about your writing, characters, or inspiration!")

user_input = st.text_input("❓ Ask a question:", "")

if st.button("Get Answer") and user_input:
    with st.spinner("Thinking..."):
        response = query_engine.query(user_input)

        st.subheader("🧠 Answer")
        st.write(response.response)

        st.subheader("📚 Sources used")
        for node in response.source_nodes:
            if node.metadata.get("file_path"):
                st.markdown(f"- **{os.path.basename(node.metadata['file_path'])}** ({node.metadata.get('source_type', 'unknown')})")