from trace import Trace
from sender import send_trace_to_backend

trace = Trace("Get today's weather")

trace.add_llm_step(
    input_prompt="What is the weather today?",
    model="gpt-4o-mini"
)

trace.add_tool_step(
    tool="weather_api",
    tool_input={"location": "New York"},
    tool_output={"temperature": "28°C"},
    latency_ms=250
)

trace.add_llm_step(
    input_prompt="Using the weather API result, answer the user's question.",
    model="gpt-4o-mini"
)

trace.finish(final_output="Today's weather is 28°C")

send_trace_to_backend(trace)