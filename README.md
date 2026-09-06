# Vigil

Vigil is an AI agent observability platform that captures agent execution traces, stores structured execution data, detects common agent failures, and provides an interactive dashboard for investigation and analysis.

AI agents often perform multiple LLM calls, invoke external tools, and make intermediate decisions before producing a final response. Looking only at the final response makes it difficult to understand how or why an agent failed.

Vigil addresses this by capturing the execution trace of an agent. The SDK records LLM calls and tool executions with prompts, outputs, token usage, latency, and execution metadata. Completed traces are sent to a FastAPI backend, stored in PostgreSQL, classified by a hybrid failure detection system, and exposed through a React dashboard.

At a high level:

```text
AI Agent
    |
    v
Vigil SDK
    |
    v
FastAPI Backend
    |
    +------------------+
    |                  |
    v                  v
PostgreSQL       Failure Classifier
                      |
              +-------+-------+
              |               |
              v               v
        Deterministic     LLM Judge
         Heuristics
              |               |
              +-------+-------+
                      |
                      v
                Classification
                      |
                      v
                 PostgreSQL
                      |
                      v
                React Dashboard
```

## Why Vigil?

AI agents are more difficult to debug than traditional applications because a single request can involve multiple model calls, tool executions, external services, and intermediate decisions.

A failure may not be visible from the final response alone. An agent may:

- repeatedly call the same tool
- repeatedly retry a failing service
- use malformed tool arguments
- exceed its available context
- follow malicious instructions returned by external content
- generate unsupported information
- gradually move away from the original user objective

Vigil makes these execution steps observable as structured traces.

This allows developers to:

- inspect how an agent reached its final response
- identify where an execution failed
- automatically classify common failure modes
- search and filter stored traces
- inspect individual execution steps
- analyze failure distributions
- evaluate classifier performance against known ground truth
- measure ingestion and retrieval performance

The goal is to make AI agent failures observable, reproducible, and measurable rather than relying only on final model outputs.

## Architecture

Vigil is organized into five primary layers.

### 1. SDK

The SDK instruments an AI agent execution.

A `Trace` records:

- agent goal
- trace ID
- timestamp
- LLM calls
- tool calls
- input prompts
- outputs
- token usage
- execution latency
- final output

### 2. FastAPI Backend

The backend receives completed traces through REST APIs.

It is responsible for:

- trace ingestion
- PostgreSQL storage
- failure classification
- trace retrieval
- filtering
- pagination
- aggregate statistics

### 3. PostgreSQL

PostgreSQL provides persistent storage for traces and their classification results.

The current application uses the `traces` table with the fields:

```text
id
trace_data
failure_mode
confidence
reasoning
agent_goal
```

Database schema evolution is managed through Alembic migrations.

### 4. Failure Classifier

The classifier uses a hybrid architecture.

Structural failures are detected with deterministic heuristics. When no heuristic identifies a failure, the trace is passed to an LLM based judge for semantic analysis.

### 5. React Dashboard

The frontend provides an interactive interface for:

- overview statistics
- trace search
- failure filtering
- confidence filtering
- pagination
- trace inspection
- execution timelines
- failure composition
- classifier performance

## Trace Capture

The SDK is centered around the `Trace` class.

A typical execution looks like:

```python
from sdk.trace import Trace
from sdk.sender import send_trace_to_backend


def weather_api(tool_input):
    return {
        "temperature": "28°C"
    }


trace = Trace("Get today's weather")

trace.add_llm_step(
    input_prompt="What is the weather today?",
    model="gpt-4o-mini"
)

weather = trace.add_tool_step(
    tool="weather_api",
    tool_function=weather_api,
    tool_input={"location": "New York"}
)

final_answer = trace.add_llm_step(
    input_prompt=f"""
The user asked:
What is the weather today?

The weather API returned:
{weather}

Answer the user's question in one sentence.
""",
    model="gpt-4o-mini"
)

trace.finish(final_output=final_answer)

send_trace_to_backend(trace)
```

### LLM Steps

Each LLM step records:

- model
- input prompt
- output text
- token count
- execution latency
- step number
- timestamp

### Tool Steps

Each tool step records:

- tool name
- tool input
- tool output
- execution latency
- step number
- timestamp

### Finalization

`Trace.finish()` records:

- final output
- failure mode
- confidence
- classifier reasoning

The completed trace can then be converted to a dictionary and sent to the backend.

## Failure Taxonomy

Vigil uses seven primary failure modes.

### Infinite Loop

Repeated calls to the same tool with identical inputs without meaningful progress.

The current heuristic detects three consecutive identical tool calls.

### Retry Storm

Repeated calls to the same tool with identical inputs after repeated failures such as timeouts or errors.

The current heuristic detects three consecutive failed calls with the same tool and input.

### Tool Misuse

Malformed or invalid tool inputs, including empty inputs and unexpected input types.

### Context Overflow

A trace whose cumulative LLM token usage exceeds the configured threshold.

The current threshold is:

```text
4000 tokens
```

### Prompt Injection

Suspicious instruction like content appearing in tool outputs, including attempts to override instructions or expose prompts and sensitive information.

### Hallucination

An agent produces unsupported or fabricated information that is not justified by the available trace evidence.

### Intent Drift

The agent gradually deviates from the original user objective.

## Hybrid Failure Classification

Vigil does not use an LLM for every classification.

The classifier first checks deterministic structural patterns:

```text
Structured Trace
      |
      v
Failure Classifier
      |
      v
Deterministic Heuristics
      |
      +---- Failure detected ----> Classification
      |
      +---- No failure detected
                  |
                  v
               LLM Judge
                  |
                  v
             Classification
```

The deterministic layer currently handles:

```text
infinite_loop
retry_storm
tool_misuse
context_overflow
prompt_injection
```

If none of these heuristics identifies a failure, the structured trace is sent to the LLM based judge for semantic analysis.

The semantic layer handles cases such as:

```text
hallucination
intent_drift
none
```

The classifier returns a failure mode along with a confidence level and reasoning. These values are stored with the trace and exposed through the dashboard.

## Backend API

The backend runs by default at:

```text
http://127.0.0.1:8000
```

Interactive FastAPI documentation is available at:

```text
http://127.0.0.1:8000/docs
```

### GET /

Health check.

Example response:

```json
{
  "message": "Vigil backend running"
}
```

### POST /traces

Receives a completed trace from the SDK.

The backend:

1. stores the raw trace
2. runs the failure classifier
3. stores the classification result
4. returns the database trace ID

Example successful response:

```json
{
  "status": "success",
  "trace_id": 123
}
```

If storage succeeds but classification fails, the trace remains stored and the endpoint returns a partial success response.

### GET /traces

Retrieves traces with support for:

- `failure_mode`
- `confidence`
- `search`
- `page`
- `limit`

Examples:

```text
/traces?page=1&limit=20
/traces?failure_mode=retry_storm
/traces?confidence=high
/traces?search=weather
/traces?failure_mode=retry_storm&confidence=high&search=weather
```

Search currently operates on `agent_goal`.

### GET /traces/{trace_id}

Retrieves one trace by database ID.

A missing trace returns HTTP 404.

### GET /stats

Returns aggregate trace statistics, including:

- total trace count
- count for each failure mode
- unclassified count

The dashboard uses this endpoint for its overview and analytics sections.

## Dashboard

The frontend is implemented using React and Vite.

### Overview

Displays:

- total traces
- total failures
- failure rate

### Trace Explorer

Provides:

- search by agent goal
- failure mode filtering
- confidence filtering
- combined filters
- pagination
- clickable trace rows

### Trace Detail

Displays:

- trace ID
- agent goal
- failure mode
- confidence
- classifier reasoning
- final output
- execution timeline

Each execution step displays the relevant metadata for an LLM call or tool call.

### Failure Analytics

Displays:

- total traces
- total failures
- failure rate
- failure composition
- classifier precision
- classifier recall
- classifier F1

## Benchmarks

Vigil was evaluated using a synthetic benchmark containing 700 traces with known ground truth labels.

The dataset distribution is:

| Category | Traces |
|---|---:|
| Clean | 350 |
| Infinite Loop | 50 |
| Retry Storm | 50 |
| Tool Misuse | 50 |
| Context Overflow | 50 |
| Prompt Injection | 50 |
| Hallucination | 50 |
| Intent Drift | 50 |
| **Total** | **700** |

### End to End Ingestion Benchmark

The complete ingestion pipeline was benchmarked with the 700 synthetic traces.

The benchmark exercises:

```text
Synthetic Trace
      |
      v
HTTP POST
      |
      v
FastAPI
      |
      v
PostgreSQL
      |
      v
Failure Classifier
      |
      v
PostgreSQL
```

Results:

| Metric | Result |
|---|---:|
| Total traces | 700 |
| Successfully processed | 700 |
| Failed requests | 0 |
| Total processing time | 654.95 seconds |
| End to end throughput | 1.07 traces/sec |

The benchmark was executed sequentially, so the result includes HTTP handling, PostgreSQL operations, deterministic classification, and LLM judge execution where applicable.

### Classifier Evaluation

Classifier predictions were compared against the 700 trace ground truth dataset using precision, recall, and F1.

| Failure Mode | Precision | Recall | F1 |
|---|---:|---:|---:|
| Infinite Loop | 100% | 100% | 100% |
| Retry Storm | 100% | 100% | 100% |
| Tool Misuse | 100% | 100% | 100% |
| Context Overflow | 100% | 100% | 100% |
| Prompt Injection | 100% | 100% | 100% |
| Hallucination | 100% | 76% | 86.36% |
| Intent Drift | 79.37% | 100% | 88.50% |

The deterministic failure modes achieved perfect scores on the synthetic benchmark because their traces were deliberately constructed around the structural patterns the heuristics are designed to detect.

The semantic failure modes produced more nuanced results.

Hallucination achieved:

```text
Precision: 100%
Recall:     76%
F1:         86.36%
```

Intent drift achieved:

```text
Precision: 79.37%
Recall:    100%
F1:         88.50%
```

### Query Latency Benchmark

Trace retrieval was benchmarked at a close to 1,000 trace scale.

The benchmark run used 767 stored traces and measured three representative query types 100 times each, for 300 API requests total.

| Query | p50 | p95 |
|---|---:|---:|
| Retrieve traces | 6.83 ms | 9.81 ms |
| Filter by failure mode | 12.26 ms | 18.57 ms |
| Filter by confidence | 9.77 ms | 11.43 ms |

After the benchmark, the database was cleaned so that only the canonical 700 synthetic benchmark traces remained.

Current database state:

```text
Total traces:     700
Synthetic traces: 700
```

## Synthetic Benchmark Dataset

The benchmark data is stored separately from the application.

### Raw Traces

```text
data/synthetic_traces.jsonl
```

Contains 700 synthetic traces without ground truth failure labels embedded in the trace data.

### Ground Truth Labels

```text
data/synthetic_labels.csv
```

Contains the expected failure mode for each synthetic trace.

The separation prevents the classifier from receiving the expected answer as part of the trace itself.

### Dataset Generator

```text
data/generate_traces.py
```

The generator creates:

- 350 clean traces
- 50 traces for each failure mode
- 700 traces total

It also validates:

- total trace count
- total label count
- unique trace IDs
- matching trace and label IDs
- absence of ground truth leakage
- expected label distribution

## Project Structure

```text
Vigil/
|
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── alembic.ini
│   └── alembic/
│       ├── env.py
│       ├── README
│       ├── script.py.mako
│       └── versions/
│
├── classifier/
│   ├── core.py
│   ├── prompt.txt
│   ├── test_traces.md
│   └── __init__.py
│
├── data/
│   ├── generate_traces.py
│   ├── synthetic_traces.jsonl
│   └── synthetic_labels.csv
│
├── frontend/
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── App.jsx
│       ├── App.css
│       ├── index.css
│       ├── main.jsx
│       └── components/
│           ├── Dashboard.jsx
│           ├── FailureAnalytics.jsx
│           ├── Header.jsx
│           ├── Sidebar.jsx
│           ├── StatCard.jsx
│           ├── TraceDetail.jsx
│           └── TraceExplorer.jsx
│
├── sdk/
│   ├── trace.py
│   ├── sender.py
│   ├── example_trace.py
│   └── __init__.py
│
├── tests/
│   ├── evaluate_classifier.py
│   ├── ingestion_benchmark.py
│   └── query_benchmark.py
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Tech Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- REST APIs

### SDK

- Python
- OpenAI API
- Requests

### Failure Classification

- OpenAI API
- GPT 4o mini
- Deterministic heuristics
- LLM based semantic judge

### Frontend

- JavaScript
- React
- JSX
- CSS
- Vite
- REST API integration

### Development Tooling

- Python virtual environment
- Node.js
- npm
- Git
- PostgreSQL

## Running Vigil

### Prerequisites

Install:

- Python
- PostgreSQL
- Node.js
- npm

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Vigil
```

### 2. Create the Python Virtual Environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Python Dependencies

From the project root:

```powershell
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root.

Set:

```env
DATABASE_URL=postgresql://<username>:<password>@localhost:<port>/<database>
OPENAI_API_KEY=<your-openai-api-key>
```

Do not commit `.env`.

### 5. Create the PostgreSQL Database

Create an empty PostgreSQL database for Vigil.

Then apply the Alembic migrations:

```powershell
cd backend
alembic upgrade head
cd ..
```

The current migration head is:

```text
a9eace39d467
```

### 6. Start the FastAPI Backend

From the project root:

```powershell
uvicorn backend.main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

FastAPI interactive documentation:

```text
http://127.0.0.1:8000/docs
```

Keep the backend running.

### 7. Start the React Dashboard

Open a second terminal.

From the project root:

```powershell
cd frontend
npm install
npm run dev
```

Open the local development URL displayed by Vite.

### 8. Run the SDK Example

Keep the backend running and open another terminal.

From the project root:

```powershell
python sdk/example_trace.py
```

The example:

1. creates a trace
2. performs an LLM call
3. performs a tool call
4. performs another LLM call
5. finalizes the trace
6. sends the trace to the backend

The backend then stores and classifies the trace.

## Benchmark Commands

### Generate the Synthetic Dataset

From the project root:

```powershell
python data/generate_traces.py
```

This regenerates:

```text
data/synthetic_traces.jsonl
data/synthetic_labels.csv
```

The generator validates the expected 700 trace distribution before saving the files.

### Evaluate the Classifier

Make sure the backend is running and the benchmark traces have been ingested.

Then run:

```powershell
python tests/evaluate_classifier.py
```

This compares the classifications stored in PostgreSQL with the synthetic ground truth labels and prints precision, recall, and F1.

### Run the Ingestion Benchmark

Make sure the backend is running.

Then run:

```powershell
python tests/ingestion_benchmark.py
```

This sends the 700 synthetic traces through the complete ingestion and classification pipeline.

Running it again will add another set of traces to the database.

### Run the Query Benchmark

Make sure the backend is running.

Then run:

```powershell
python tests/query_benchmark.py
```

This measures p50 and p95 latency for representative trace retrieval queries.

## End to End Flow

A typical Vigil execution follows this path:

```text
User Request
     |
     v
AI Agent
     |
     +----> LLM Call
     |
     +----> Tool Call
     |
     +----> LLM Call
     |
     v
Vigil SDK
     |
     | Structured Trace
     v
FastAPI Backend
     |
     +----> PostgreSQL
     |
     +----> Failure Classifier
                    |
             +------+------+
             |             |
             v             v
        Heuristics      LLM Judge
             |             |
             +------+------+
                    |
                    v
              Classification
                    |
                    v
               PostgreSQL
                    |
                    v
             React Dashboard
```

The SDK observes the agent while it executes.

The backend stores the completed trace.

The classifier analyzes the execution.

The dashboard exposes the resulting trace and classification for investigation.

## Final Summary

Vigil combines AI agent instrumentation, trace storage, hybrid failure detection, benchmarking, and interactive visualization into one observability platform.

The SDK captures LLM calls and tool executions as structured traces and sends them to a FastAPI backend. PostgreSQL provides persistent storage, while the failure classifier combines deterministic heuristics with an LLM based judge.

The platform detects seven primary failure modes:

```text
infinite_loop
retry_storm
tool_misuse
context_overflow
prompt_injection
hallucination
intent_drift
```

A synthetic benchmark containing 700 traces provides a reproducible environment for measuring classifier accuracy. Separate ingestion and retrieval benchmarks measure system performance.

The React dashboard provides a visual interface for searching traces, inspecting execution timelines, analyzing failures, and understanding agent behavior from the original goal through the final output.

Vigil is designed to make AI agent execution observable, failure detection measurable, and debugging easier than relying only on final model outputs.

## License

Vigil is released under the MIT License. See `LICENSE` for details.
