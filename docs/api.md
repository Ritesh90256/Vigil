# Vigil API Documentation

Base URL: `http://127.0.0.1:8000`

---

## Endpoints

### GET /
Health check — confirms the backend is running.

**Request:** No parameters required.

**Response:**
```json
{
  "message": "Vigil backend running"
}
```

---

### POST /traces
Receives a captured trace from the Vigil SDK and stores it in PostgreSQL.

**Request body:**
```json
{
  "input": "What is the capital of France?",
  "output": "The capital of France is Paris.",
  "latency": 2761
}
```

| Field | Type | Description |
|---|---|---|
| input | string | The prompt sent to the LLM or the input passed to the tool |
| output | string | The response from the LLM or the output returned by the tool |
| latency | integer | Time taken for the call in milliseconds |

**Response:**
```json
{
  "status": "stored"
}
```

---

### GET /traces
Returns all stored traces from the database.

**Request:** No parameters required.

**Response:**
```json
[
  {
    "id": 1,
    "input": "What is the capital of France?",
    "output": "The capital of France is Paris.",
    "latency": 2761,
    "created_at": "2026-06-05T10:30:00"
  },
  {
    "id": 2,
    "input": "search_weather({'city': 'bangalore'})",
    "output": "28°C, partly cloudy",
    "latency": 0,
    "created_at": "2026-06-05T10:30:01"
  }
]
```

---

### GET /traces/{trace_id}
Returns a single trace by its ID.

**Path parameter:**

| Parameter | Type | Description |
|---|---|---|
| trace_id | integer | The ID of the trace to retrieve |

**Example request:**
GET /127.0.0.1:8000/traces/1

**Response — trace found:**
```json
{
  "id": 1,
  "input": "What is the capital of France?",
  "output": "The capital of France is Paris.",
  "latency": 2761,
  "created_at": "2026-06-05T10:30:00"
}
```

**Response — trace not found:**
```json
{
  "error": "Trace not found"
}
```

---

## Database Schema

Table name: `traces`

| Column | Type | Description |
|---|---|---|
| id | integer | Auto-incremented primary key |
| input | text | Input prompt or tool input |
| output | text | LLM response or tool output |
| latency | integer | Call duration in milliseconds |
| created_at | timestamp | When the trace was stored |

---

## Running the Backend

```bash
uvicorn backend.main:app --reload
```

API will be available at `http://127.0.0.1:8000`

Interactive docs available at `http://127.0.0.1:8000/docs`

---

## Notes

- The DATABASE_URL is currently hardcoded — move to .env before deploying
- The POST /traces endpoint accepts any dict — input validation will be added in Week 2
- Classifier endpoint POST /traces/{id}/classify will be added in Week 2