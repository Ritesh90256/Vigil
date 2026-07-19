from enum import Enum
class FailureMode(str, Enum):
    HALLUCINATION = "hallucination"
    TOOL_MISUSE = "tool_misuse"
    INFINITE_LOOP = "infinite_loop"
    PROMPT_INJECTION = "prompt_injection"
    CONTEXT_OVERFLOW = "context_overflow"
    INTENT_DRIFT = "intent_drift"
    RETRY_STORM = "retry_storm"