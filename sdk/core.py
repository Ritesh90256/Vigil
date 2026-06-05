import time
import json
from datetime import datetime, timezone
import openai
import requests

# Backend endpoint where all traces are sent for storage and analysis
BACKEND_URL = "http://127.0.0.1:8000/traces"


def send_trace_to_backend(trace: dict):
    """
    Sends a captured trace to the Vigil backend via HTTP POST.
    Fails silently if the backend is not running — SDK still works locally.
    """
    try:
        response = requests.post(BACKEND_URL, json={
            "input": trace.get("input_prompt") or str(trace.get("tool_input")),
            "output": trace.get("output_text") or str(trace.get("tool_output")),
            "latency": int(trace.get("latency_ms", 0))
        })
        print("Sent to backend:", response.json())
    except Exception as e:
        # Backend unavailable — trace still captured locally
        print(f"Backend unavailable, trace captured locally: {e}")


def capture_llm_call(prompt: str, model: str = "gpt-4o-mini") -> dict:
    """
    Wraps an OpenAI API call and captures a structured trace.

    Captures:
    - input_prompt: what was sent to the LLM
    - output_text: what the LLM returned
    - latency_ms: round-trip time to OpenAI in milliseconds
    - token_count: total tokens consumed (input + output)
    - failure_mode: null until the Vigil classifier runs in Week 2

    Returns the trace as a Python dict.
    """
    start_time = time.time()

    response = openai.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    # latency measured as total round-trip time including network + model inference
    latency_ms = round((time.time() - start_time) * 1000, 2)

    trace = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "type": "llm_call",
        "model": model,
        "input_prompt": prompt,
        "output_text": response.choices[0].message.content,
        "latency_ms": latency_ms,
        # total_tokens includes both prompt tokens and completion tokens
        "token_count": response.usage.total_tokens,
        "failure_mode": None
    }

    print(json.dumps(trace, indent=2))
    send_trace_to_backend(trace)

    return trace


def capture_tool_call(tool_name: str, tool_input: dict, tool_output, latency_ms: float = 0.0) -> dict:
    """
    Captures a tool call made by an agent.

    Note: latency_ms should be measured by the caller around the actual tool
    execution, since the tool runs outside this function. Pass it in explicitly.

    Captures:
    - tool_name: which tool was called
    - tool_input: the arguments passed to the tool
    - tool_output: what the tool returned
    - latency_ms: how long the tool took to execute (passed in by caller)
    - failure_mode: null until the Vigil classifier runs in Week 2
    """
    trace = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "type": "tool_call",
        "tool_name": tool_name,
        "tool_input": tool_input,
        # tool_output cast to string to handle any return type
        "tool_output": str(tool_output),
        "latency_ms": latency_ms,
        "failure_mode": None
    }

    print(json.dumps(trace, indent=2))
    send_trace_to_backend(trace)

    return trace