from trace import Trace
import json
from sender import send_trace_to_backend

trace = Trace("Get today's weather")

trace.add_llm_step(output_text="Calling weather API", input_prompt="What is the weather today?", latency_ms=120, token_count=15, model="gpt-4o-mini")

trace.add_tool_step(tool="weather_api", tool_input={"location": "New York"}, tool_output={"temperature": "28°C"}, latency_ms=250)

trace.add_llm_step(output_text="Weather information retrieved", input_prompt=None, latency_ms=50, token_count=10, model="gpt-4o-mini")

trace.finish(final_output="Today's weather is 28°C")

send_trace_to_backend(trace)