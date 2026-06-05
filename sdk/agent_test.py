import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sdk.core import capture_llm_call, capture_tool_call


# --- Tool definitions ---

def calculator(expression: str) -> str:
    """
    Evaluates a mathematical expression and returns the result as a string.
    Uses eval() which is safe here since we control the input.
    """
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


def search_weather(city: str) -> str:
    """
    Mock weather tool — returns hardcoded weather data for known cities.
    In production this would call a real weather API.
    """
    weather_data = {
        "bangalore": "28°C, partly cloudy",
        "mumbai": "32°C, humid",
        "delhi": "35°C, sunny"
    }
    return weather_data.get(city.lower(), "Weather data not found")


# --- Agent ---

def run_agent(user_query: str) -> dict:
    """
    A simple 3-step agent that demonstrates multi-step trace capture:
    Step 1 — LLM decides which tool to use
    Step 2 — Tool is called, latency measured externally and passed to SDK
    Step 3 — LLM uses tool result to answer the user
    """
    print(f"\n{'='*50}")
    print(f"Agent starting for query: {user_query}")
    print(f"{'='*50}\n")

    full_trace = {
        "agent_goal": user_query,
        "steps": []
    }

    # Step 1 — LLM decides what to do
    step1 = capture_llm_call(
        f"User asked: '{user_query}'. What tool should I use? "
        f"Reply with just the tool name and input. "
        f"Options: calculator(expression) or search_weather(city)"
    )
    step1["step"] = 1
    full_trace["steps"].append(step1)

    # Step 2 — Call the appropriate tool
    # Latency is measured here, outside capture_tool_call,
    # because the tool executes outside the SDK
    if "weather" in user_query.lower():
        city = "bangalore"
        if "delhi" in user_query.lower():
            city = "delhi"
        elif "mumbai" in user_query.lower():
            city = "mumbai"

        tool_start = time.time()
        weather_result = search_weather(city)
        tool_latency = round((time.time() - tool_start) * 1000, 2)

        step2 = capture_tool_call(
            tool_name="search_weather",
            tool_input={"city": city},
            tool_output=weather_result,
            latency_ms=tool_latency
        )

    else:
        # Default expression — can be extended to parse query dynamically
        expression = "15 * 24"
        if "45" in user_query:
            expression = "45 * 67"
        elif "120" in user_query:
            expression = "120 / 5"

        tool_start = time.time()
        calc_result = calculator(expression)
        tool_latency = round((time.time() - tool_start) * 1000, 2)

        step2 = capture_tool_call(
            tool_name="calculator",
            tool_input={"expression": expression},
            tool_output=calc_result,
            latency_ms=tool_latency
        )

    step2["step"] = 2
    full_trace["steps"].append(step2)

    # Step 3 — LLM uses tool result to give final answer
    step3 = capture_llm_call(
        f"Tool returned: {step2['tool_output']}. "
        f"Now answer the user's question: '{user_query}'"
    )
    step3["step"] = 3
    full_trace["steps"].append(step3)

    print(f"\n{'='*50}")
    print("Full agent trace complete — 3 steps captured")
    print(f"{'='*50}\n")

    return full_trace


if __name__ == "__main__":
    queries = [
        "What is the weather in Bangalore?",
        "What is 45 * 67?",
        "What is the weather in Delhi?",
        "What is 120 / 5?",
        "Tell me the weather in Mumbai"
    ]

    for query in queries:
        run_agent(query)