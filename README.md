# Prompt2Slide Engine

A professional AI-powered presentation generator that creates PowerPoint slides from natural language prompts using RAG (Retrieval Augmented Generation) and Stable Diffusion.

## 🚀 Overview

This engine combines three core technologies:
1.  **LLM (Phi-3 Mini):** Generates structured slide content (titles, bullet points) based on context.
2.  **RAG (FAISS + m SentenceTransformers):** Retrieves relevant Islamic or ML context to inform the slide content.
3.  **Image Engine (Stable Diffusion v1.5):** Generates educational illustrations for each slide.
4.  **PPT Generator:** Assemblies everything into a professional PowerPoint (`.pptx`) file.

## 📁 Project Structure

```text
prompt2slides/
├── app/                    # Core engine package
│   ├── rag/                # RAG implementation & retrieval
│   ├── llm/                # LLM loader and generation logic
│   ├── router/             # Domain router (Islamic vs ML)
│   ├── embeddings/         # FAISS indices and text data
│   ├── prompts/            # Prompt templates
│   ├── image_engine.py      # Stable Diffusion image generation
│   └── app.py              # Main 'ask' interface
├── ppt_generator.py         # PowerPoint creation utility
├── prompt2slide_api.py      # FastAPI server
└── test_generation.py       # Quick test script
```

## 🛠 Setup

1.  **Create Virtual Environment:**
    ```bash
    python -m venv .venv
    .\.venv\Scripts\activate
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 🖥 Usage

### Run a Test Generation
```bash
python test_generation.py
```
This will generate a one-slide presentation `test_output.pptx` in the root directory.

### Start the API Server
```bash
uvicorn prompt2slide_api:app --reload
```

## 🔧 Optimization Notes

-   **CPU vs GPU:** The system automatically detects CUDA. On CPU-only systems, the LLM runs in 32-bit mode and Stable Diffusion will be significantly slower.
-   **Structure:** The project has been refactored into a modular `app` package for easier maintenance and testing.
