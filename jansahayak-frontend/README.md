# JanSahayak Frontend

Next.js 16 + Tailwind CSS 4 + TypeScript chat interface for JanSahayak.

## Setup

```bash
cd jansahayak-frontend

# Install dependencies
npm install
```

## Run

```bash
# Development (HMR enabled)
npm run dev

# Production build
npm run build
npm start
```

## Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start Next.js dev server (port 3000) |
| `npm run build` | Create production build |
| `npm start` | Serve production build |
| `npm run lint` | Run ESLint |

## Environment Variables

Create a `.env.local` file in the `jansahayak-frontend/` root:

| Variable | Description | Required |
|----------|-------------|----------|
| `NEXT_PUBLIC_API_BACKEND_URL` | Backend API base URL (exposed to browser) | Yes (default: `http://localhost:5000`) |
| `HUGGINGFACE_API_KEY` | HuggingFace API key (server-side only) | No |

> **Note:** Variables prefixed with `NEXT_PUBLIC_` are exposed to the browser. All others are server-side only.

## Tech Stack

- **Framework:** Next.js 16 (App Router)
- **Styling:** Tailwind CSS 4
- **Language:** TypeScript 5
- **HTTP Client:** Axios
- **Markdown:** react-markdown + rehype-raw + remark-gfm
- **Icons:** react-icons
