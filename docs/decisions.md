# Vigil:Architecture Decision Records

## ADR-001: Programming Language

**Decision:** Python
**Options:** Python, TypeScript, Go
**Reason:** Python provides the strongest ecosystem for LLM development, including LangChain, OpenAI SDK, and Anthropic SDK support. It enables faster development and is the language most familiar to the team.

---

## ADR-002: Backend Framework

**Decision:** FastAPI
**Options:** FastAPI, Flask, Django
**Reason:** FastAPI offers high performance, built-in asynchronous support, automatic API documentation generation, and a lightweight architecture suitable for building APIs quickly.

---

## ADR-003: Database

**Decision:** PostgreSQL
**Options:** PostgreSQL, MongoDB, SQLite
**Reason:** Vigil's trace and failure data is structured and fits naturally into a relational database. PostgreSQL is reliable, free to run locally, and can easily scale to cloud deployments later.

---

## ADR-004: Tracing Standard

**Decision:** OpenTelemetry-inspired structure
**Options:** Custom trace format, OpenTelemetry standard
**Reason:** OpenTelemetry is the industry standard for distributed tracing and observability. Adopting its concepts makes Vigil compatible with existing monitoring tools and industry practices.

---

## ADR-005: SDK Testing LLM

**Decision:** OpenAI GPT-4o-mini
**Options:** OpenAI, Anthropic, Google Gemini
**Reason:** OpenAI models are widely used by startups and AI teams. Supporting GPT-4o-mini ensures the SDK works with a common production setup while remaining cost-effective during development.

---

## ADR-006: Failure Classifier LLM

**Decision:** Anthropic Claude Sonnet
**Options:** GPT-4o, Claude Sonnet, Open-source models
**Reason:** Claude Sonnet performs strongly on structured classification tasks and consistently follows output formatting requirements. This reliability is important when assigning failures to a single category with confidence scores.

---

## ADR-007: Project Management Platform

**Decision:** Huly
**Options:** Huly
**Reason:** Huly is the project management platform required by PVL and is used for task tracking, collaboration, and progress management throughout development.

---

## ADR-008: Dashboard Framework (Future)

**Decision:** Next.js
**Options:** React, Next.js, Vue
**Reason:** Next.js is a widely adopted framework for production dashboards, offering a strong component ecosystem, routing support, and excellent developer experience for future frontend development.
