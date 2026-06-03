import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sdk.core import capture_llm_call, capture_tool_call
import openai

# --- Define simple tools ---

def calculator(expression: str) -> str:
    """A simple calculator tool"""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

def search_weather(city: str) -> str:
    """A mock weather search tool"""
    # Mock response — no real API needed
    weather_data = {
        "bangalore": "28°C, partly cloudy",
        "mumbai": "32°C, humid",
        "delhi": "35°C, sunny"
    }
    return weather_data.get(city.lower(), "Weather data not found")

# --- Run a multi-step agent ---

def run_agent(user_query: str):
    """
    A simple agent that:
    1. Receives a query
    2. Decides which tool to use
    3. Calls the tool
    4. Returns final answer
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
        f"User asked: '{user_query}'. What tool should I use? Reply with just the tool name and input. Options: calculator(expression) or search_weather(city)"
    )
    step1["step"] = 1
    full_trace["steps"].append(step1)
    
    # Step 2 — Call the appropriate tool based on query
    if "weather" in user_query.lower():
        tool_result = capture_tool_call(
            tool_name="search_weather",
            tool_input={"city": "bangalore"},
            tool_output=search_weather("bangalore")
        )
    else:
        tool_result = capture_tool_call(
            tool_name="calculator",
            tool_input={"expression": "15 * 24"},
            tool_output=calculator("15 * 24")
        )
    
    tool_result["step"] = 2
    full_trace["steps"].append(tool_result)
    
    # Step 3 — LLM uses tool result to give final answer
    step3 = capture_llm_call(
        f"Tool returned: {tool_result['tool_output']}. Now answer the user's question: '{user_query}'"
    )
    step3["step"] = 3
    full_trace["steps"].append(step3)
    
    print(f"\n{'='*50}")
    print("Full agent trace complete — 3 steps captured")
    print(f"{'='*50}\n")
    
    return full_trace

if __name__ == "__main__":
    # Test 1 — weather query
    run_agent("What is the weather in Bangalore?")
    
    # Test 2 — math query  
    run_agent("What is 15 multiplied by 24?")