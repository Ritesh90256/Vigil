from typing import Optional
import uuid
from datetime import datetime, timezone
import time
import openai

class Trace:
    """Represents one complete AI agent execution.

    A Trace starts when the user's request begins and
    accumulates every LLM call and tool call until the
    final response is produced.
    """
    def __init__ (self, agent_goal: str):
        self.trace = {
            "trace_id" : str(uuid.uuid4()),
            "timestamp" : datetime.now(timezone.utc).isoformat(),
            "agent_goal" : agent_goal,
            "steps" : [],
            "final_output" : None,
            "failure_mode" : None,
            "confidence" : None,
            "reasoning" : None
        }
    
    def add_llm_step(self, input_prompt: str, model: str = "gpt-4o-mini"):
        """
        Calls the LLM, captures the metadata, and records the step
        in the trace.
        """

        # Start timing the LLM call
        start_time = time.time()

        # Make the OpenAI API call
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": input_prompt
                }
            ]
        )

        # Measure latency
        latency_ms = round((time.time() - start_time) * 1000, 2)

        # Extract response information
        output_text = response.choices[0].message.content
        token_count = response.usage.total_tokens

        # Add this LLM call as a step in the trace
        self.trace["steps"].append({
            "step": len(self.trace["steps"]) + 1,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "type": "llm_call",
            "model": model,
            "input_prompt": input_prompt,
            "output_text": output_text,
            "latency_ms": latency_ms,
            "token_count": token_count,
        })

        # Return the LLM's response so the agent can continue
        return output_text
    
    
    def add_tool_step(self,tool:str,tool_function,tool_input: dict):
        start_time = time.time()
        tool_output = tool_function(tool_input)
        latency_ms = round((time.time() - start_time)*1000, 2)
        
        self.trace["steps"].append({
            "step": len(self.trace["steps"]) + 1,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "type": "tool_call",
            "tool_name": tool,
            "tool_input": tool_input,
            "tool_output": tool_output,
            "latency_ms": latency_ms,

        })

        return tool_output


    def finish(self, final_output:str, failure_mode:str=None, confidence:str=None, reasoning:str=None):
        self.trace["final_output"] = final_output
        self.trace["failure_mode"] = failure_mode
        self.trace["confidence"] = confidence
        self.trace["reasoning"] = reasoning
        return self.trace
    
    
    def to_dict(self):
        return self.trace
