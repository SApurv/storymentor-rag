from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.together import TogetherLLM
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever

import chromadb
import os
from dotenv import load_dotenv

# 📦 Load environment variables
load_dotenv()

# 🧠 Set embedding model
Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 🔑 Set LLM
Settings.llm = TogetherLLM(
    api_key=os.getenv("TOGETHER_API_KEY"),
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    temperature=0.7,
    max_tokens=512
)

# 🧠 Custom system prompt
custom_prompt = """
You are a personalized creative writing assistant for me.

You have access to the following knowledge sources:
- `my_story`: samples of the my past writing — analyze these deeply to understand their tone, feel, style, and voice.
- `writing_guide`: practical writing advice, especially for structure, pacing, grammar, and storytelling techniques.
- `book`: inspiration for plot ideas, tropes, character arcs — use with discretion and never copy directly.

When answering:
- Always incorporate relevant information retrieved from these sources.
- Prioritize alignment with the my existing style and tone.
- If my request is vague, ask follow-up questions to understand my intent better.
- Be collaborative: your job is to enhance the my story ideas, not override them.

Never generate generic advice — every answer should feel personalized and grounded in retrieved content.

"""
def ask_question():
    chroma_client = chromadb.PersistentClient(path="./chroma_store")
    collection = chroma_client.get_or_create_collection("story_docs")
    vector_store = ChromaVectorStore(chroma_collection=collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)

    # ✅ Custom retriever with metadata filtering
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=5
    )

    query_engine = RetrieverQueryEngine.from_args(
        retriever=retriever,
        system_prompt=custom_prompt
    )

    print("📚 Your writing assistant is ready! Type your questions below.\n")

    while True:
        query = input("❓ Ask something (or type 'exit'): ")
        if query.lower() in ['exit', 'quit']:
            break

        response = query_engine.query(query)

        print("\n🧠 Answer:\n")
        print(response.response)

        print("\n📚 Sources used:")
        for node in response.source_nodes:
            if node.metadata.get("file_path"):
                print(f"- {os.path.basename(node.metadata['file_path'])} ({node.metadata.get('source_type', 'unknown')})")
        print("\n" + "-" * 60)

if __name__ == "__main__":
    ask_question()