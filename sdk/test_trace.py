from trace import Trace
from sender import send_trace_to_backend

trace = Trace("Get today's weather")

trace.add_llm_step(
    input_prompt="What is the weather today?",
    model="gpt-4o-mini"
)

def weather_api(tool_input):
    return{
        "temperature":"28°C"
    }

weather = trace.add_tool_step(
    tool = "weather_api",
    tool_function = weather_api,
    tool_input = {"location": "New York"}
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

trace.finish(final_output = final_answer)

send_trace_to_backend(trace)