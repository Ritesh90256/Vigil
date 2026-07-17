from typing import Optional
import uuid
from datetime import datetime, timezone

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
    
    def add_llm_step(self, input_prompt: Optional[str], output_text: str, latency_ms: float, token_count: int, model: str):
        """Adds a step representing an LLM call to the trace."""
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
    
    def add_tool_step(self, tool:str, tool_input:str, tool_output:str, latency_ms:float):
        """Adds a step representing a tool call to the trace."""
        self.trace["steps"].append({
            "step": len(self.trace["steps"]) + 1,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "type": "tool_call",
            "tool_name": tool,
            "tool_input": tool_input,
            "tool_output": tool_output,
            "latency_ms": latency_ms,

        })

    def finish(self, final_output:str, failure_mode:str=None, confidence:str=None, reasoning:str=None):
        self.trace["final_output"] = final_output
        self.trace["failure_mode"] = failure_mode
        self.trace["confidence"] = confidence
        self.trace["reasoning"] = reasoning
        return self.trace
    
    def to_dict(self):
        return self.trace
