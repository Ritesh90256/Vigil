# Vigil — AI Agent Observability

> Real-time failure detection for LLM-powered agents.

Most companies deploying AI agents have no way to know when their agents are 
hallucinating, misusing tools, or drifting from user intent, until a customer 
complains. Existing tools log traces. None of them tell you what went wrong and why.

Vigil does.

---

## What it does

Vigil captures every LLM call, tool use, and reasoning step your agent makes, 
then automatically classifies what went wrong.

**7 failure modes detected:**
- Hallucination
- Tool misuse
- Infinite loop
- Prompt injection
- Context overflow
- Intent drift
- Retry storm

---

## Architecture
Agent Code
↓
Vigil SDK          ← captures LLM calls + tool calls
↓
FastAPI Backend    ← receives and stores traces
↓
PostgreSQL         ← trace storage
↓
Classifier         ← labels failure mode (Week 2)
↓
Dashboard          ← visualise traces and failures (Week 5)

---

## Quick Start

**1. Install dependencies**
```bash
pip install openai requests
```

**2. Set your OpenAI API key**
```bash
set OPENAI_API_KEY=your_key_here
```

**3. Start the backend**
```bash
uvicorn backend.main:app --reload
```

**4. Add to your agent**
```python
from sdk.core import capture_llm_call, capture_tool_call

# Capture an LLM call
trace = capture_llm_call("What is the capital of France?")

# Capture a tool call
trace = capture_tool_call(
    tool_name="search_weather",
    tool_input={"city": "bangalore"},
    tool_output="28°C, partly cloudy",
    latency_ms=12.5
)
```

---

## Project Structure
vigil/
├── sdk/              # Python SDK:captures agent traces
├── backend/          # FastAPI server + PostgreSQL storage
├── classifier/       # Failure detection engine (Week 2)
├── dashboard/        # Next.js trace viewer (Week 5)
├── data/
│   ├── raw/          # Collected agent traces
│   └── labeled/      # Labeled dataset for classifier training
├── docs/             # Architecture, decisions, taxonomy
└── tests/            # Test scripts

---

## Team

Ritesh, Sami M, Samhith R Gowda
PESU Venture Labs : ABC 2026

---

## Status

| Component | Status |
|---|---|
| SDK — LLM call capture | ✅ Done |
| SDK — Tool call capture | ✅ Done |
| Backend — FastAPI + PostgreSQL | ✅ Done |
| Classifier | 🔄 Week 2 |
| Dashboard | 🔄 Week 5 |