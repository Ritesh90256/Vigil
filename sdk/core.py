import time
import json
from datetime import datetime, timezone
import openai
import requests

def send_trace_to_backend(trace: dict):
    try:
        url = "http://127.0.0.1:8000/traces"
        response = requests.post(url, json={
            "input": trace.get("input_prompt") or str(trace.get("tool_input")),
            "output": trace.get("output_text") or str(trace.get("tool_output")),
            "latency": int(trace.get("latency_ms", 0))
        })
        print("Sent to backend:", response.json())
    except Exception as e:
        print("Failed to send trace:", e)

def capture_llm_call(prompt: str, model: str = "gpt-4o-mini") -> dict:
    """
    Wraps an OpenAI API call and captures trace data.
    Returns both the response and the captured trace.
    """

    # Record start time before the call
    start_time = time.time()

    # Make the actual OpenAI call
    response = openai.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    # Record end time after the call
    end_time = time.time()

    # Calculate latency in milliseconds
    latency_ms = round((end_time - start_time) * 1000, 2)

    # Extract the output text from response
    output_text = response.choices[0].message.content

    # Extract token count from response
    token_count = response.usage.total_tokens

    # Build the trace as structured JSON
    trace = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "type": "llm_call",
        "model": model,
        "input_prompt": prompt,
        "output_text": output_text,
        "latency_ms": latency_ms,
        "token_count": token_count,
        "failure_mode": None
    }

    # Print trace as formatted JSON
    print(json.dumps(trace, indent=2))
    send_trace_to_backend(trace)

    return trace


def capture_tool_call(tool_name: str, tool_input: dict, tool_output) -> dict:
    """
    Captures a tool call made by an agent.
    """

    # Record start time
    start_time = time.time()

    # Record end time
    end_time = time.time()

    # Calculate latency
    latency_ms = round((end_time - start_time) * 1000, 2)

    # Build the trace
    trace = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "type": "tool_call",
        "tool_name": tool_name,
        "tool_input": tool_input,
        "tool_output": str(tool_output),
        "latency_ms": latency_ms,
        "failure_mode": None
    }

    # Print trace as formatted JSON
    print(json.dumps(trace, indent=2))
    send_trace_to_backend(trace)

    return trace


# Test it with a real call
if __name__ == "__main__":
    result = capture_llm_call("What is the capital of France?")