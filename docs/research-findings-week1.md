# Research Findings – Week 1

## 1. Most Agent Failures Are Not Model Failures

While collecting and labeling traces, we observed that many failures were caused by workflow issues rather than poor model reasoning.

Examples:

- Wrong tool selected
- Lost context between steps
- Infinite retry loops
- Incorrect task routing

### Implication for Vigil

Observability must capture the entire agent workflow, not just the final model response.

---

## 2. Multi-Step Agents Fail More Often Than Single-Step Agents

Single prompt → single answer systems are relatively easy to monitor.

Failures increase when agents:

- Use tools
- Call APIs
- Delegate tasks
- Maintain memory

### Example

A research agent successfully retrieved information, but the writer agent never received the context.

Result:

- Incorrect report
- No obvious error message

### Implication for Vigil

Tracing agent steps is as important as tracing model outputs.

---

## 3. Failure Modes Repeat Across Different Frameworks

While reviewing examples inspired by:

- AutoGPT
- LangChain
- CrewAI
- LangGraph

we observed similar failures repeatedly.

Common patterns:

| Failure          | Frequency |
| ---------------- | --------- |
| Tool Misuse      | High      |
| Hallucination    | High      |
| Context Loss     | High      |
| Intent Drift     | Medium    |
| Retry Storms     | Medium    |
| Prompt Injection | Medium    |
| Infinite Loops   | Medium    |

### Implication

A small failure taxonomy can explain a large percentage of agent failures.

---

## 4. Real Companies Face These Problems

### Air Canada

Problem:
Chatbot provided incorrect refund information.

Result:
Legal dispute.

Failure Type:
Hallucination.

---

### AutoGPT Users

Problem:
Agents repeatedly performed actions without progressing.

Failure Type:
Infinite Loop.

---

### Enterprise Agent Platforms

Problem:
Agents choose incorrect tools or lose context between steps.

Failure Types:

- Tool Misuse
- Context Loss

---

### Implication

These failures already exist in production systems and create business risk.

---

## 5. Agent Observability Is Still Early

Most teams can see:

- Logs
- API requests
- Errors

Very few can answer:

> Why did the agent fail?

or

> Which step caused the failure?

### Implication

Vigil's classifier can provide higher-level explanations instead of raw logs.

---

# Key Takeaway

After analyzing 50 labeled traces, we found that a relatively small set of recurring failure modes explains most agent failures.

These findings validate Vigil's approach:

1. Capture complete execution traces.
2. Detect recurring failure patterns.
3. Classify failures automatically.
4. Help teams understand why an agent failed.
