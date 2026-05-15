# SHL AI Assessment Recommendation System

## Overview

This project is a conversational AI recommendation system that suggests relevant SHL assessments based on hiring requirements and natural language queries.

The system supports:
- semantic assessment retrieval
- conversational refinement
- clarification handling
- comparison queries
- refusal handling
- recruiter-style responses

---

## Tech Stack

- Python
- FastAPI
- Sentence Transformers
- FAISS
- Gemini API

---

## Features

- Semantic search using embeddings
- FAISS vector retrieval
- Conversational recommendations
- Comparison handling
- Refinement-aware retrieval
- Prompt injection protection
- Off-topic refusal handling

---

## API Endpoints

### GET /health

Returns API health status.

### POST /chat

Accepts conversational queries and returns:
- reply
- recommendations
- end_of_conversation

---

## Example Request

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hiring backend Java engineers with AWS skills"
    }
  ]
}
```

---

## Run Locally

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run API

```bash
python -m uvicorn app:app
```

---

## Project Structure

```text
shl-ai-agent/
│
├── app.py
├── retrieval.py
├── llm.py
├── prompts.py
├── conversation.py
├── refinement.py
├── comparison.py
├── guardrails.py
├── embed.py
├── scraper.py
├── catalog.json
├── requirements.txt
├── README.md
```