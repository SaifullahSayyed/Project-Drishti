# DRISHTI

Predictive Justice & Case Resolution Engine.

## Overview

DRISHTI is a FastAPI-based backend (with a modern frontend) that predicts case timelines, recommends resolution pathways, and surfaces relevant precedents for Indian courts. It orchestrates live case data, statistical models, RAG with Groq, and Indian Kanoon search into a single API.

## Tech Stack

- Backend: FastAPI, SQLAlchemy (async), Pydantic Settings
- AI / ML: XGBoost, pandas, joblib, Groq LLMs
- Data / Search: PostgreSQL, Redis, Pinecone (optional), Indian Kanoon API

## Backend Setup (Local)

1. Create and activate venv
   ```bash
   python -m venv backend/venv
   backend/venv/Scripts/activate  # Windows PowerShell
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment
   - Copy `.env.example` to `.env`
   - Fill in the real values for:
     - `DATABASE_URL`
     - `REDIS_URL`
     - `GROQ_API_KEY`
     - `PINECONE_API_KEY`
     - `PINECONE_INDEX_NAME`
     - `HUGGINGFACE_TOKEN`
     - `INDIAN_KANOON_API_KEY`
     - `SECRET_KEY`

4. Run the API
   ```bash
   uvicorn backend.main:app --reload --port 8000
   ```

The health check is available at `http://localhost:8000/health`.
