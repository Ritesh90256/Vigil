# Vigil

Vigil is an open source observability platform for AI agents. It captures the internal execution of an agent, stores structured traces, and automatically detects common failure modes.

AI agents often perform multiple LLM calls, invoke external tools, and make intermediate decisions before producing a final response. Looking only at the final response makes it difficult to understand how or why an agent failed.

Vigil addresses this by capturing the complete execution trace of an agent. The SDK records LLM calls and tool executions along with prompts, outputs, token usage, latency, and other execution metadata. These traces are sent to a FastAPI backend, stored in PostgreSQL, and analyzed by a hybrid failure classifier.

The classifier combines deterministic heuristics for structurally identifiable failures with an LLM based judge for failures that require semantic analysis. The resulting classifications, confidence scores, and reasoning can then be explored through the Vigil dashboard.

At a high level, the system follows:

AI Agent → Vigil SDK → FastAPI → PostgreSQL → Failure Classifier → Dashboard

## Why Vigil?

AI agents are more difficult to debug than traditional applications because a single user request can involve multiple LLM calls, tool executions, external services, and intermediate decisions.

A failure may not be visible from the final response alone. An agent can produce an incorrect result because it repeatedly calls a tool, retries a failing service, passes invalid arguments, exceeds its available context, follows malicious instructions returned by a tool, generates unsupported information, or gradually moves away from the user's original goal.

Vigil provides visibility into these intermediate execution steps by capturing them as structured traces.

This allows developers to:

- inspect how an agent reached its final response
- identify where an execution failed
- automatically classify common failure modes
- retrieve and filter stored traces
- analyze failure patterns and system performance
- evaluate the accuracy of failure detection using ground truth data

The goal is to make AI agent failures observable, reproducible, and measurable rather than relying only on the final model output.

## Architecture

Vigil is organized as a pipeline that follows an AI agent execution from trace capture to failure analysis and visualization.

```text
AI Agent
   |
   | LLM calls and tool executions
   v
Vigil SDK
   |
   | Structured trace
   v
FastAPI Backend
   |
   +------------------+
   |                  |
   v                  v
PostgreSQL       Failure Classifier
                      |
                +-----+-----+
                |           |
                v           v
           Heuristics    LLM Judge
                |           |
                +-----+-----+
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

### Trace Capture

The Vigil SDK runs alongside an AI agent and records its execution as a structured trace. Each trace contains the agent goal, execution steps, LLM calls, tool calls, latency, token usage, inputs, outputs, and final response.

### Ingestion

The completed trace is sent to the FastAPI backend through a REST API. The backend stores the trace in PostgreSQL and passes it to the failure classifier.

### Failure Classification

The classifier first applies deterministic heuristics for failure modes that can be identified from structured trace patterns. When no heuristic identifies a failure, the trace can be passed to the LLM based judge for semantic classification.

### Dashboard

The React dashboard retrieves the stored trace and classification data through REST APIs and presents it through trace exploration, failure analysis, execution timelines, and aggregate metrics.

## Trace Capture

Vigil provides an SDK for capturing AI agent execution with minimal integration.

A trace records the agent's goal and the sequence of operations performed during an execution. LLM calls and tool calls are represented as structured steps with the metadata required for debugging and failure analysis.

Each LLM step can capture:

- model used
- input prompt
- output text
- token count
- execution latency

Each tool step can capture:

- tool name
- tool input
- tool output
- execution latency

A completed trace is serialized into a structured JSON payload and sent to the Vigil backend through the trace sender.

This allows the SDK to remain focused on observing the agent while the backend and classifier handle storage, analysis, and failure detection.

## Failure Taxonomy

Vigil uses a seven mode failure taxonomy to classify common failure patterns in AI agent executions.

### Infinite Loop

Detects repeated calls to the same tool with identical inputs in sequence.

### Retry Storm

Detects rapid repeated attempts to call the same tool with identical inputs when the tool repeatedly fails.

### Tool Misuse

Detects tool calls with malformed or unexpected arguments, including invalid input types and empty inputs.

### Context Overflow

Detects traces whose cumulative LLM token usage exceeds the configured threshold. The current implementation uses a 4,000 token threshold.

### Prompt Injection

Detects suspicious instruction like patterns appearing inside tool outputs, including attempts to override instructions or expose prompts and sensitive information.

### Hallucination

Identifies responses that contain information unsupported by the available trace evidence or retrieved tool results.

### Intent Drift

Identifies cases where the agent's behavior deviates from the original objective of the user request.

The first five failure modes are currently handled by deterministic heuristics. Hallucination and intent drift are handled by the LLM based judge when they are not detected by the deterministic layer.

## Hybrid Failure Classification

Vigil uses a hybrid approach to failure detection. The classifier first applies deterministic heuristics to the structured trace and uses an LLM based judge when the trace is not matched by the available heuristics.

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
The deterministic layer is used for failure modes that can be identified from explicit patterns in the trace. This provides fast and predictable detection without requiring an LLM call.

The current deterministic heuristics detect:

Infinite Loop
Retry Storm
Tool Misuse
Context Overflow
Prompt Injection

When none of these heuristics identifies a failure, the trace is passed to the LLM based judge. The judge receives the structured trace and evaluates behavior that requires semantic reasoning, such as hallucination and intent drift.

The classifier returns a failure mode along with a confidence level and reasoning that can be stored with the trace and displayed through the dashboard.

## Backend and Storage

### FastAPI

FastAPI provides the REST API layer for Vigil. It receives completed traces from the SDK, stores them, runs failure classification, and exposes the stored data for retrieval and analysis.

The backend currently supports:

- trace ingestion through `POST /traces`
- trace retrieval through `GET /traces`
- filtering by failure mode
- filtering by confidence
- pagination
- retrieving an individual trace by ID
- aggregate trace statistics

The backend connects the trace capture layer with PostgreSQL and the failure classifier.

### PostgreSQL

PostgreSQL provides persistent storage for captured traces and their classification results.

The database is designed around core observability concepts including:

- `traces`
- `spans`
- `tool_calls`
- `labels`

The `traces` data contains the overall agent execution, while spans and tool call records provide more detailed execution information that can be used for trace inspection and visualization.

## Dashboard

Vigil includes a React based dashboard for exploring AI agent traces and analyzing detected failures.

The dashboard communicates with the FastAPI backend through REST APIs and presents stored trace and classification data through an interactive interface.

The dashboard provides:

- overview statistics for stored traces and detected failures
- trace search and filtering
- failure mode and confidence filtering
- individual trace inspection
- visualization of LLM and tool execution steps
- execution latency and token usage information
- classifier reasoning and confidence
- failure distribution and performance analytics

The trace detail view presents an agent execution as a sequence of operations, making it possible to follow the path from the original objective through LLM calls and tool executions to the final output and detected failure.

The dashboard provides the primary interface for investigating agent behavior without requiring developers to inspect raw JSON responses or query the PostgreSQL database directly.

## Benchmarks

Vigil was evaluated using a synthetic benchmark dataset containing 700 AI agent traces with known ground truth labels across seven failure modes.

### Trace Ingestion

The complete trace ingestion pipeline was benchmarked using 700 synthetic traces.

The benchmark exercised the full backend path:

```text
Trace
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

## Results:

**700 / 700 traces successfully processed**
**0 failed requests**
**654.95 seconds total processing time**
**1.07 traces/sec end to end throughput**

The benchmark was run sequentially, so the measured throughput includes HTTP handling, PostgreSQL operations, deterministic classification, and LLM judge execution where applicable.

## Failure Classification

The classifier was evaluated against the 700 trace ground truth dataset using precision, recall, and F1 for each failure mode.

| Failure Mode     |  Precision |   Recall |         F1 |
| ---------------- | ---------: | -------: | ---------: |
| Infinite Loop    |   **100%** | **100%** |   **100%** |
| Retry Storm      |   **100%** | **100%** |   **100%** |
| Tool Misuse      |   **100%** | **100%** |   **100%** |
| Context Overflow |   **100%** | **100%** |   **100%** |
| Prompt Injection |   **100%** | **100%** |   **100%** |
| Hallucination    |   **100%** |  **76%** | **86.36%** |
| Intent Drift     | **79.37%** | **100%** | **88.50%** |

The deterministic heuristics achieved perfect scores on the synthetic benchmark because the corresponding traces were deliberately constructed around the structural patterns they are designed to detect.

The semantic failure modes produced more nuanced results. **Hallucination** achieved **100% precision** and **76% recall**, while **intent drift** achieved **79.37% precision** and **100% recall**.

## Query and Retrieval Latency

Trace retrieval was benchmarked through the FastAPI retrieval API against a PostgreSQL database containing **767 stored traces**.

Three representative query types were each **executed 100 times**, resulting in **300 API retrieval requests**.

| Query                  |          p50 |          p95 |
| ---------------------- | -----------: | -----------: |
| Retrieve traces        |  **6.83 ms** |  **9.81 ms** |
| Filter by failure mode | **12.26 ms** | **18.57 ms** |
| Filter by confidence   |  **9.77 ms** | **11.43 ms** |

These measurements include the HTTP request, FastAPI processing, PostgreSQL query execution, and response generation.

## Synthetic Benchmark Dataset

Vigil includes a synthetic benchmark dataset designed to evaluate failure detection against known ground truth.

The dataset contains 700 synthetic AI agent traces:

| Category | Number of Traces |
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

The benchmark stores the raw traces separately from their ground truth labels.

The raw traces contain only the information that would be available to the classifier during a real execution. The ground truth dataset stores the expected failure mode for each trace and is used only during evaluation.

This separation allows classifier predictions to be compared against known labels without exposing the expected answer to the classifier.

## Project Structure

```text
Vigil/
│
├── sdk/
│   ├── trace.py
│   ├── sender.py
│   └── test_trace.py
│
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   └── schema.sql
│
├── classifier/
│   ├── core.py
│   ├── prompt.txt
│   └── batch_classify.py
│
├── data/
│   ├── generate_trace.py
│   ├── synthetic_traces.jsonl
│   └── synthetic_labels.csv
│
├── tests/
│   ├── ingestion_benchmark.py
│   ├── evaluate_classifier.py
│   └── query_benchmark.py
│
├── frontend/
│   └── React dashboard
│
└── README.md
```

## Tech Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- REST APIs

### AI and Classification

- OpenAI API
- GPT 4o mini
- Deterministic failure detection heuristics

### Frontend

- JavaScript
- React
- JSX
- CSS
- REST API integration

### Development Tooling

- Node.js
- npm

## Running Vigil

### Start the Backend

From the project root:

```bash
uvicorn backend.main:app --reload
```

The FastAPI backend runs at:
```bash
http://127.0.0.1:8000
```
FastAPI's interactive API documentation is available at:
```bash
http://127.0.0.1:8000/docs
```
### Run the SDK Trace Example

From the project root:
```bash
python sdk/test_trace.py
```
This runs a sample agent workflow through the Vigil SDK. The SDK captures the execution trace and sends it to the FastAPI ingestion endpoint.

### Generate the Synthetic Benchmark Dataset
```bash
python data/generate_trace.py
```
This generates 700 synthetic traces and their corresponding ground truth labels for classifier evaluation.

### Evaluate the Classifier
```bash
python tests/evaluate_classifier.py
```
This compares the classifier predictions stored in PostgreSQL with the synthetic ground truth labels and calculates precision, recall, and F1 for each failure mode.

### Run the Ingestion Benchmark
```bash
python tests/ingestion_benchmark.py
```
This measures the throughput of the end to end trace ingestion and classification pipeline.

### Run the Query Latency Benchmark
```bash
python tests/query_benchmark.py
```
This measures trace retrieval latency through the FastAPI API and reports p50 and p95 latency for representative queries.

## End to End Example

A typical Vigil execution follows this flow:

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
             +----+----+
             |         |
             v         v
        Heuristics  LLM Judge
             |         |
             +----+----+
                  |
                  v
         Failure Classification
                  |
                  v
              PostgreSQL
                  |
                  v
           React Dashboard
```

The SDK observes the agent while it executes the user's request and records the LLM and tool interactions that occur during the execution.

The completed trace is sent to the FastAPI backend, where it is stored in PostgreSQL and analyzed by the failure classifier.

The classifier first checks deterministic heuristics for structurally identifiable failures. When no heuristic identifies a failure, the trace can be passed to the LLM based judge for semantic analysis.

The resulting failure mode, confidence, reasoning, and execution data are then available through the dashboard for investigation and analysis.

## Project Summary

Vigil combines AI agent instrumentation, trace storage, failure detection, benchmarking, and interactive visualization into a single observability platform.

The SDK captures LLM calls and tool executions as structured traces and sends them to a FastAPI backend. PostgreSQL provides persistent storage, while a hybrid failure classifier combines deterministic heuristics with an LLM based judge to identify common agent failures.

The platform supports seven failure modes: infinite loop, retry storm, tool misuse, context overflow, prompt injection, hallucination, and intent drift.

A synthetic benchmark containing 700 labeled traces provides a reproducible environment for evaluating the classifier using precision, recall, and F1. Separate ingestion and retrieval benchmarks measure system performance under realistic workloads.

The React dashboard provides a visual interface for exploring traces, inspecting execution steps, analyzing detected failures, and understanding agent behavior from the initial goal through the final output.

Vigil is designed to make AI agent execution observable, failure detection measurable, and debugging significantly easier than relying on final model outputs alone.
