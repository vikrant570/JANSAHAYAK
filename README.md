# JANSAHAYAK

AI-powered civic assistant that recommends government schemes based on user queries and profiles.

## Architecture

```
jansahayak-frontend/  →  jansahayak-backend/  →  jansahayak-ai/
   Next.js :3000           Express :5000          FastAPI :8000
```

## AI Response Flow

The core prompt → response cycle passes through three functions across the stack:

```
┌─────────────────────────────────────────────────────────────────────┐
│  1. handleSend()                                                    │
│     File: jansahayak-frontend/src/components/PromptBar.tsx  L:101   │
│     User types a prompt and clicks send.                            │
│     POSTs { prompt, chatID } to backend /agent/chat via Axios.      │
│                              │                                      │
│                              ▼                                      │
│  2. router.post("/chat", ...)                                       │
│     File: jansahayak-backend/src/routes/agentGateway.ts     L:10    │
│     Extracts prompt & chatID from req.body.                         │
│     Resolves user profile from JWT cookie.                          │
│     Saves user message to MongoDB.                                  │
│     Forwards { query, profile, top_k } to AI engine /api/v1/chat.   │
│     Saves AI response to MongoDB.                                   │
│     Returns { status, answer } to frontend.                         │
│                              │                                      │
│                              ▼                                      │
│  3. async def chat()                                                │
│     File: jansahayak-ai/app/main.py                         L:244   │
│     Detects intent (greeting / scheme_query / unrelated).           │
│     For scheme queries: runs FAISS RAG + ranking + explanation.     │
│     Formats results into a single Markdown string.                  │
│     Returns { status: "success", answer: "<markdown>" }.            │
└─────────────────────────────────────────────────────────────────────┘
```

### Data Flow Summary

| Step | Layer | Function | File | Line |
|------|-------|----------|------|------|
| 1 | Frontend | `handleSend()` | `PromptBar.tsx` | 101 |
| 2 | Backend | `router.post("/chat", ...)` | `agentGateway.ts` | 10 |
| 3 | AI Engine | `async def chat()` | `main.py` | 244 |

## Quick Start

```bash
# Terminal 1 — AI Engine
cd jansahayak-ai
.\venv\Scripts\activate
uvicorn app.main:app --port 8000 --reload

# Terminal 2 — Backend
cd jansahayak-backend
npm run dev

# Terminal 3 — Frontend
cd jansahayak-frontend
npm run dev
```

## Project Structure

```
JANSAHAYAK/
├── jansahayak-frontend/   # Next.js 16 + Tailwind + TypeScript
├── jansahayak-backend/    # Express 5 + TypeScript + MongoDB
└── jansahayak-ai/         # FastAPI + FAISS + Sentence Transformers
```
