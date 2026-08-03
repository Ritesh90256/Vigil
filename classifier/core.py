import os
import json
from pathlib import Path
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

PROMPT_PATH = Path(__file__).parent / "prompt.txt"


def load_prompt():
    """Reads the prompt template from prompt.txt"""
    with open(PROMPT_PATH, "r") as f:
        return f.read()


def build_prompt(trace):
    """Inserts a trace's JSON into the prompt template"""
    prompt_template = load_prompt()

    return prompt_template.replace(
        "{trace_json}",
        json.dumps(trace, indent=2)
    )

def detect_infinite_loop(trace: dict):

    steps = trace.get("steps",[])

    previous_tool = None
    previous_input = None
    repeat_count = 1

    for step in steps:

        if step.get("type") != "tool_call":
            continue
        current_tool = step.get("tool_name")
        current_input = step.get("tool_input")

        if (
            current_tool == previous_tool and 
            current_input == previous_input
            ):
            repeat_count += 1
        else:
            repeat_count = 1

        if repeat_count >=3:
            return {
                "failure_mode" : "infinite_loop",
                "confidence" : "high",
                "reasoning" : "Detected three consecutive identical tool calls with the same input."
            }
        previous_tool = current_tool
        previous_input = current_input

    return None


def classify_trace(trace: dict, model: str = "gpt-4o-mini") -> dict:

    heuristic_result = detect_infinite_loop(trace)
    if heuristic_result:
        return heuristic_result
    
    prompt = build_prompt(trace)

    response = openai.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0  # deterministic — same trace always gives same result
    )

    raw_output = response.choices[0].message.content
    cleaned = raw_output.strip()

    # LLMs sometimes wrap JSON in markdown code fences despite instructions
    # not to — strip that out before parsing
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]

    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError:
        # Don't crash the whole batch run if one response is malformed —
        # return a clear marker instead so you can investigate later
        result = {
            "failure_mode": "unknown",
            "confidence": "low",
            "reasoning": f"Failed to parse LLM response: {raw_output}"
        }

    return result


if __name__ == "__main__":
    # Quick manual test with one trace before running the full batch
    sample_trace = {
        "trace_id": "demo",
        "agent_goal": "Retrieve weather data",
        "steps": [
            {
                "step": 1,
                "type": "tool_call",
                "tool_name": "weather_api",
                "tool_input": {"location": "New York"},
                "tool_output": {"temperature": "28°C"}
            },
            {
                "step": 2,
                "type": "tool_call",
                "tool_name": "weather_api",
                "tool_input": {"location": "New York"},
                "tool_output": {"temperature": "28°C"}
            },
            {
                "step": 3,
                "type": "tool_call",
                "tool_name": "weather_api",
                "tool_input": {"location": "New York"},
                "tool_output": {"temperature": "28°C"}
            }
        ],
        "final_output": "No answer generated"
    }

    result = classify_trace(sample_trace)
    print(json.dumps(result, indent=2))