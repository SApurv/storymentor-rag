# ✨ StoryMentor: Your AI-Powered Writing Assistant ✍️

**StoryMentor** is a personalized, RAG-based AI writing assistant that understands your style, integrates your favorite books and writing guides, and helps you craft better stories.

---

## 💡 What It Does

- 🧠 **Understands your writing style** by analyzing your past stories.
- 📚 **Learns from books** you admire to help with plot inspiration.
- 📖 **Follows writing guides** to give you professional, tailored tips.
- 💬 Runs locally or with a cloud LLM (via [Together AI](https://www.together.ai/)).
- 🎛️ Query it in real time via a Streamlit UI or CLI.

---

## 🔍 How It Works

StoryMentor is built on a Retrieval-Augmented Generation (RAG) pipeline using:
- **LlamaIndex** for indexing and querying
- **Chroma** for vector store
- **Together AI (Mixtral)** as the backend LLM
- **HuggingFace embeddings** (MiniLM) for fast vector generation

The app intelligently uses **metadata tags** (e.g., `my_story`, `writing_guide`, `book`) to provide the most context-aware answers.

---

## 🛠️ Setup Instructions

1. **Clone the repository**
    ```bash
    git clone https://github.com/your-username/storymentor-rag.git
    cd storymentor-rag
    ```

2. **Create a virtual environment & install dependencies**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # or .venv\Scripts\activate on Windows
    pip install -r requirements.txt
    ```

4. **Add your environment variables**
    ```env
    Create a .env file with:
    TOGETHER_API_KEY=your_api_key_here
    ```

6. **Prepare your data**
    ```kotlin
    data/
    ├── My_stories/
    ├── Books/
    └── Writing_guides/
    ```
   
8. **Build the vector index**
    ```bash
    python build_index.py
    ```

10. **Ask questions!**
     ```bash
     python query_engine.py
     ```
     
OR deploy via Streamlit (instructions below 👇)

---

## 🌐 Deploy on Streamlit

1. **Create a secrets.toml inside .streamlit/:**
     ```toml
     TOGETHER_API_KEY = "your_api_key_here"
     ```

3. **Run Streamlit locally:**
    ```bash
    streamlit run app.py
    ```

5. **Or deploy on Streamlit Cloud**

---

## 🧠 Example Prompt
“Can you help me pace my new story plot better? I want to retain my writing voice and take some structural inspiration from the guides and books I’ve uploaded.”

---

## 🙋 Why This Project?
As a passionate amateur writer with tech + AI skills, I built this to:
1. Get tailored feedback based on my own stories
2. Integrate guides/books without manually flipping through them
3. Explore how RAG and LLMs can enhance creative writing

---

## 📌 Tech Stack
* LlamaIndex
* HuggingFace Embeddings
* Together AI (Mixtral / LLaMA)
* ChromaDB
* Python + Streamlit

---

## 🚀 Future Plans
* Add feedback/rating on responses
* Improve writing style detection
* Add PDF/Docx reader support
* Add story versioning support


