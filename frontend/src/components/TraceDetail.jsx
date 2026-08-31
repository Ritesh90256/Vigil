import { useEffect, useState } from "react"

const API_URL = "http://127.0.0.1:8000"

function TraceDetail({ traceId }) {
  const [trace, setTrace] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    setLoading(true)
    setError(null)
    setTrace(null)

    fetch(`${API_URL}/traces/${traceId}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Trace not found")
        }

        return response.json()
      })
      .then((data) => {
        setTrace(data)
      })
      .catch((error) => {
        console.error(error)
        setError("Failed to load trace.")
      })
      .finally(() => {
        setLoading(false)
      })
  }, [traceId])

  if (loading) {
    return <p>Loading trace...</p>
  }

  if (error) {
    return <p>{error}</p>
  }

  if (!trace) {
    return <p>Trace not found.</p>
  }

  return (
    <section className="trace-detail">
      <h2>Trace Detail</h2>

      <p>Trace ID: {trace.id}</p>
      <p>Agent Goal: {trace.agent_goal}</p>
      <p>Failure Mode: {trace.failure_mode}</p>
      <p>Confidence: {trace.confidence}</p>
      <p>Reasoning: {trace.reasoning}</p>
      <p>Final Output: {trace.trace_data?.final_output}</p>

      <h3>Execution Steps</h3>

      <div className="execution-steps">
        {trace.trace_data.steps.map((step) => (
          <div className="execution-step" key={step.step}>
            <strong>
              Step {step.step}: {step.type}
            </strong>

            {step.type === "llm_call" && (
              <div>
                <p>Model: {step.model}</p>
                <p>Tokens: {step.token_count}</p>
                <p>Latency: {step.latency_ms} ms</p>
              </div>
            )}

            {step.type === "tool_call" && (
              <div>
                <p>Tool: {step.tool_name}</p>
                <p>Latency: {step.latency_ms} ms</p>
              </div>
            )}
          </div>
        ))}
      </div>
    </section>
  )
}

export default TraceDetail