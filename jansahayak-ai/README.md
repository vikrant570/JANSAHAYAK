# JanSahayak AI Engine

Python-based AI service powering JanSahayak's scheme recommendation and chat system. Built with **FastAPI**, **FAISS**, **Sentence Transformers**, and **Pydantic**.

## Setup

```bash
cd jansahayak-ai

# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --port 8000 --reload
```

## Environment Variables

Create a `.env` file in the `jansahayak-ai/` root (see `.env.example`):

| Variable | Description | Required |
|----------|-------------|----------|
| `APP_NAME` | Application display name | No (default: `JanSahayak AI`) |
| `APP_VERSION` | Semantic version string | No (default: `1.0.0`) |
| `LLM_PROVIDER` | LLM backend — `mock`, `openai`, `gemini` | No (default: `mock`) |
| `LLM_MODEL` | Model identifier for the chosen provider | No |
| `OPENAI_API_KEY` | OpenAI API key (if provider is `openai`) | Conditional |
| `GEMINI_API_KEY` | Gemini API key (if provider is `gemini`) | Conditional |
| `INDIA_GOV_SCHEME_URL` | Gov scheme search endpoint | No |
| `MYSCHEME_SCHEME_URL` | MyScheme search endpoint | No |
| `MYSCHEME_API_KEY` | MyScheme API key | No |
| `TESSERACT_CMD` | Path to Tesseract OCR binary | No |
| `HF_TOKEN` | Hugging Face token | No |
| `CORS_ORIGINS` | Comma-separated allowed origins | No |
| `EMBEDDING_MODEL` | Sentence-transformer model name | No (default: `all-MiniLM-L6-v2`) |
| `MAX_FILE_SIZE_MB` | Max upload size in MB | No (default: `10`) |

## Key Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| `GET` | `/` | Service status |
| `GET` | `/api/v1/health` | Health check |
| `POST` | `/api/v1/chat` | Chat endpoint (returns markdown) |
| `POST` | `/api/v1/recommendations` | Structured JSON recommendations |
