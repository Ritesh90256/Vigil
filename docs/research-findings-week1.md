# Research Findings – Week 1

## Dataset Summary
- Total traces labeled: 50
- Traces with no failure: 10
- Traces with failures: 40

### Failure Mode Distribution

| Failure Mode     | Count | % of failures |
|-----------------|-------|---------------|
| Tool Misuse      | 11    | 27.5%         |
| Context Overflow | 8     | 20%           |
| Hallucination    | 7     | 17.5%         |
| Intent Drift     | 6     | 15%           |
| Infinite Loop    | 5     | 12.5%         |
| Prompt Injection | 4     | 10%           |
| Retry Storm      | 2     | 5%            |

**Most common failure: Tool Misuse (27.5% of all failures)**
**Second most common: Context Overflow (20%)**

---

## Key Finding 1 — Most Agent Failures Are Not Model Failures
Failures were caused by workflow issues rather than poor model reasoning.
Examples:
- Wrong tool selected
- Lost context between steps
- Infinite retry loops
- Incorrect task routing

**Implication for Vigil:** Observability must capture the entire agent
workflow, not just the final model response.

---

## Key Finding 2 — Multi-Step Agents Fail More Often
Single prompt → single answer systems are easy to monitor.
Failures increase when agents use tools, call APIs, delegate tasks,
or maintain memory across steps.

**Example:** A research agent retrieved information successfully but the
writer agent never received the context — incorrect report, no error message.

**Implication for Vigil:** Tracing individual steps is as important
as tracing model outputs.

---

## Key Finding 3 — A Small Taxonomy Explains Most Failures
7 failure modes cover 100% of the failures observed in 50 traces.
Same patterns appeared across AutoGPT, LangChain, CrewAI, and LangGraph
inspired traces — failure modes are framework-agnostic.

**Implication:** Vigil's 7-mode classifier can explain the majority
of real-world agent failures without needing a custom taxonomy per team.

---

## Key Finding 4 — Real Companies Face These Problems
- **Air Canada** — chatbot hallucinated refund policy, led to legal dispute
- **AutoGPT users** — infinite loops in production, widely documented on GitHub
- **Enterprise agent platforms** — tool misuse and context loss are the
  top reported issues in LangSmith GitHub issues

**Implication:** These are not edge cases — they are production risks
with real business consequences.

---

## Key Finding 5 — Agent Observability Is Still Early
Most teams can see logs, API requests, and errors.
Very few can answer:
- Why did the agent fail?
- Which step caused the failure?
- How often does this failure happen?

**Implication:** Vigil's classifier provides higher-level explanations
instead of raw logs — this is the gap no free tool currently fills.

---

## Mentor Feedback — Week 1
Our mentor advised us to take a step back from building and focus on
understanding the market first. Key points:

- Building is the easy part — understanding who the customer is and
  where the product fits in the market is harder and more important
- We need to validate that the problem is real before optimizing the solution
- Phase 1 is about discovery, not delivery

**Action taken:** We have begun structured market research following
PVL's 8-step Problem Discovery framework — industry map, stakeholder
analysis, competitor complaints, and customer definition documents
are being built in parallel with the technical work.

---

## What We Still Don't Know
- Who is our most specific target customer — solo developer, small
  startup, or mid-size company?
- What does a real startup's agent failure look like vs our synthetic traces?
- Why don't teams just use LangSmith — what specifically makes them
  stay or leave?
- How much time do engineers actually spend debugging agent failures per week?

These questions will be answered through direct startup conversations
in Week 2.

---

## Key Takeaway
50 labeled traces show that 7 failure modes explain 100% of agent
failures observed. Tool misuse and context overflow are the most
common. The market has logging tools — nobody has a free,
open-source classifier that automatically tells you what failed and why.
That is Vigil's gap.