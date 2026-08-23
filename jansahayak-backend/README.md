# JanSahayak Backend

Express.js + TypeScript API server. Handles authentication, chat persistence, and proxies prompts to the AI engine.

## Setup

```bash
cd jansahayak-backend

# Install dependencies
npm install

# Create .env (see below for variables)
cp .env.example .env   # or create manually
```

## Run

```bash
# Development (auto-reload + env loaded)
npm run dev

# Production
npm run build
npm start
```

## Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start dev server with `--watch` and `--env-file` |
| `npm run build` | Compile TypeScript to `dist/` |
| `npm start` | Run compiled JS from `dist/` |

## Environment Variables

Create a `.env` file in the `jansahayak-backend/` root:

| Variable | Description | Required |
|----------|-------------|----------|
| `PORT` | Server port | Yes (default: `5000`) |
| `NODE_ENV` | `development` or `production` | Yes |
| `CLIENT_URL` | Frontend origin for CORS | Yes |
| `DB_URL` | MongoDB connection string | Yes |
| `JWT_SECRET` | Secret key for signing JWTs | Yes |
| `SMTP_EMAIL` | Gmail address for sending emails | Yes |
| `SMTP_PASS` | Gmail app password | Yes |
| `AI_API_BASE_URL` | AI engine base URL | Yes (default: `http://127.0.0.1:8000`) |
| `AI_ENGINE_URL` | Alternate AI engine URL | No |

## Tech Stack

- **Runtime:** Node.js 22+
- **Framework:** Express 5
- **Language:** TypeScript 7
- **Database:** MongoDB (Mongoose 9)
- **Auth:** JWT + bcrypt + OTP verification
- **Email:** Nodemailer (Gmail SMTP)
- **Dev runner:** tsx (with Node `--watch`)
