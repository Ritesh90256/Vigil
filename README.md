# Vigil

Vigil is an observability platform for AI agents that automatically captures execution traces, stores them, and detects common failure modes using deterministic heuristics and LLM-based classification.

## Features

- SDK for one-line trace capture
- FastAPI ingestion service
- PostgreSQL trace storage
- Failure-mode classification
- Deterministic heuristics
- Extensible architecture for additional detectors

## Current Failure Modes

Implemented heuristics:

- Infinite Loop
- Retry Storm
- Tool Misuse
- Context Overflow
- Prompt Injection

LLM fallback:

- GPT-4o-mini classifier for complex or unknown failures

## Project Structure

```
Vigil/
│
├── sdk/
│
├── backend/
│
├── classifier/
│
└── frontend/ (planned)
```

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- OpenAI API
- React (planned)

## Running the Project

### Backend

```
uvicorn backend.main:app --reload
```

### SDK Test

```
python sdk/test_trace.py
```

## Roadmap

- React dashboard
- Span visualization
- Trace search
- Additional failure heuristics
- Metrics and analytics