# Vigil SDK

A lightweight Python wrapper that captures LLM calls and tool calls from your AI agent and sends them to the Vigil backend for storage and failure analysis.

---

## Installation

```bash
pip install openai requests
```

Set your OpenAI API key:
```bash
# Windows
set OPENAI_API_KEY=your_key_here

# Mac/Linux
export OPENAI_API_KEY=your_key_here
```

---

## Usage

### Capture an LLM call

```python
from sdk.core import capture_llm_call

trace = capture_llm_call("What is the capital of France?")
```

### Capture a tool call

```python
from sdk.core import capture_tool_call

trace = capture_tool_call(
    tool_name="search_weather",
    tool_input={"city": "bangalore"},
    tool_output="28°C, partly cloudy"
)
```

### Full multi-step agent trace

```python
from sdk.core import capture_llm_call, capture_tool_call

# Step 1 — LLM decides what to do
capture_llm_call("What should I do to find the weather in Bangalore?")

# Step 2 — Tool is called
capture_tool_call(
    tool_name="search_weather",
    tool_input={"city": "bangalore"},
    tool_output="28°C, partly cloudy"
)

# Step 3 — LLM uses tool result to answer
capture_llm_call("Weather is 28°C. Tell the user.")
```

---

## What it captures

### LLM calls
| Field | Description |
|---|---|
| timestamp | When the call happened (UTC) |
| type | Always "llm_call" |
| model | LLM model used (e.g. gpt-4o-mini) |
| input_prompt | The prompt sent to the LLM |
| output_text | The response from the LLM |
| latency_ms | How long the call took in milliseconds |
| token_count | Total tokens used |
| failure_mode | Null until classifier runs |

### Tool calls
| Field | Description |
|---|---|
| timestamp | When the call happened (UTC) |
| type | Always "tool_call" |
| tool_name | Name of the tool called |
| tool_input | Input passed to the tool |
| tool_output | Output returned by the tool |
| latency_ms | How long the call took in milliseconds |
| failure_mode | Null until classifier runs |

---

## How it works

Every call to `capture_llm_call` or `capture_tool_call`:
1. Records start time
2. Executes the call
3. Records end time and calculates latency
4. Builds a structured JSON trace
5. Prints the trace to console
6. Automatically sends the trace to the Vigil backend at `http://127.0.0.1:8000/traces`

---

## Backend requirement

The Vigil backend must be running locally before traces can be stored:

```bash
uvicorn backend.main:app --reload
```

If the backend is not running, the SDK will still capture and print traces — it just won't store them.

---

## Files

| File | Description |
|---|---|
| core.py | Main SDK — capture functions |
| agent_test.py | Test agent demonstrating multi-step trace capture |
| README.md | This file |