# Vigil Trace Labeling Guide

## Purpose
This guide ensures traces are labeled consistently.

## Labels

### none
Agent successfully completed the task.

### hallucination
Agent generated unsupported or incorrect information.

### tool_misuse
Agent selected the wrong tool or used a tool incorrectly.

### infinite_loop
Agent repeatedly performed the same action without progress.

### prompt_injection
External instructions overrode the intended task.

### context_overflow
Important context was lost, forgotten, or unavailable.

### intent_drift
Agent deviated from the original user goal.

### retry_storm
Agent repeatedly retried a failing operation.

## Labeling Process

1. Read the trace.
2. Identify the agent goal.
3. Determine whether the goal was achieved.
4. Find the primary failure.
5. Assign one label only.
6. If no failure exists, assign none.