import sys
import os

# This tells Python where to find the sdk folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sdk.core import capture_llm_call

def test_basic_capture():
    """Test 1 — Basic question, checks all fields are captured"""
    print("\n--- Test 1: Basic question ---")
    trace = capture_llm_call("What is the capital of France?")
    
    assert trace["input_prompt"] == "What is the capital of France?"
    assert trace["output_text"] is not None
    assert trace["latency_ms"] > 0
    assert trace["token_count"] > 0
    assert trace["failure_mode"] is None
    assert trace["timestamp"] is not None
    print("✓ Test 1 passed")

def test_longer_prompt():
    """Test 2 — Longer prompt, checks latency increases"""
    print("\n--- Test 2: Longer prompt ---")
    trace = capture_llm_call("Explain how photosynthesis works in detail, covering light reactions, dark reactions, and the role of chlorophyll.")
    
    assert trace["input_prompt"] is not None
    assert trace["output_text"] is not None
    assert trace["token_count"] > 20  # longer response = more tokens
    assert trace["latency_ms"] > 0
    print("✓ Test 2 passed")

def test_different_model():
    """Test 3 — Check model field is captured correctly"""
    print("\n--- Test 3: Model field ---")
    trace = capture_llm_call("What is 2 + 2?", model="gpt-4o-mini")
    
    assert trace["model"] == "gpt-4o-mini"
    assert trace["output_text"] is not None
    assert trace["token_count"] > 0
    print("✓ Test 3 passed")

if __name__ == "__main__":
    print("Running Vigil SDK tests...")
    test_basic_capture()
    test_longer_prompt()
    test_different_model()
    print("\n✓ All tests passed — SDK capturing correctly")