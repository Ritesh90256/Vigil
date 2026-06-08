import json
from pathlib import Path

PROMPT_PATH = Path(__file__).parent / "prompt.txt"


def load_prompt():
    with open(PROMPT_PATH, "r") as f:
        return f.read()


def build_prompt(trace):
    prompt_template = load_prompt()

    return prompt_template.replace(
        "{trace_json}",
        json.dumps(trace, indent=2)
    )


if __name__ == "__main__":
    sample_trace = {
        "trace_id": "demo",
        "steps": [
            {"step": 1, "action": "search"},
            {"step": 2, "action": "search"}
        ]
    }

    prompt = build_prompt(sample_trace)

    print(prompt)