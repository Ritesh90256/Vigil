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
        return <p className="status-message">Loading trace...</p>
    }

    if (error) {
        return <p className="status-message">{error}</p>
    }

    if (!trace) {
        return <p className="status-message">Trace not found.</p>
    }

    const failureClass = trace.failure_mode === "none" ? "success" : "failure"

    return (
        <section className="trace-detail">
            <div className="trace-detail-header">
                <h2>Trace Detail</h2>

                <div className="trace-meta-grid">
                    <div className="trace-meta-item">
                        <div className="trace-meta-label">Trace ID</div>
                        <div className="trace-meta-value">{trace.id}</div>
                    </div>

                    <div className="trace-meta-item">
                        <div className="trace-meta-label">Confidence</div>
                        <div className="trace-meta-value success">{trace.confidence}</div>
                    </div>

                    <div className="trace-meta-item full-width">
                        <div className="trace-meta-label">Agent Goal</div>
                        <div className="trace-meta-value">{trace.agent_goal}</div>
                    </div>

                    <div className="trace-meta-item">
                        <div className="trace-meta-label">Failure Mode</div>
                        <div className={`trace-meta-value ${failureClass}`}>
                            {trace.failure_mode.replaceAll("_", " ")}
                        </div>
                    </div>

                    <div className="trace-meta-item">
                        <div className="trace-meta-label">Reasoning</div>
                        <div className="trace-meta-value">{trace.reasoning}</div>
                    </div>

                    <div className="trace-meta-item full-width">
                        <div className="trace-meta-label">Final Output</div>
                        <div className="trace-meta-value">
                            {trace.trace_data?.final_output}
                        </div>
                    </div>
                </div>
            </div>

            <div className="execution-section">
                <h3>Execution Timeline</h3>

                <div className="execution-steps">
                    {trace.trace_data.steps.map((step, index) => {
                        const isTool = step.type === "tool_call"

                        return (
                            <div className="timeline-item" key={step.step}>
                                <div className={`execution-step ${isTool ? "tool-step" : ""}`}>
                                    <div className="execution-step-header">
                                        <div className="execution-step-title">
                                            Step {step.step}
                                        </div>

                                        <div className="execution-step-type">
                                            {isTool ? "Tool Call" : "LLM Call"}
                                        </div>
                                    </div>

                                    <div className="execution-step-info">
                                        {isTool ? (
                                            <>
                                                <div className="execution-info-item">
                                                    <div className="execution-info-label">Tool</div>
                                                    <div className="execution-info-value">
                                                        {step.tool_name}
                                                    </div>
                                                </div>

                                                <div className="execution-info-item">
                                                    <div className="execution-info-label">Latency</div>
                                                    <div className="execution-info-value">
                                                        {step.latency_ms} ms
                                                    </div>
                                                </div>
                                            </>
                                        ) : (
                                            <>
                                                <div className="execution-info-item">
                                                    <div className="execution-info-label">Model</div>
                                                    <div className="execution-info-value">
                                                        {step.model}
                                                    </div>
                                                </div>

                                                <div className="execution-info-item">
                                                    <div className="execution-info-label">Tokens</div>
                                                    <div className="execution-info-value">
                                                        {step.token_count}
                                                    </div>
                                                </div>

                                                <div className="execution-info-item">
                                                    <div className="execution-info-label">Latency</div>
                                                    <div className="execution-info-value">
                                                        {step.latency_ms} ms
                                                    </div>
                                                </div>
                                            </>
                                        )}
                                    </div>
                                </div>

                                {index < trace.trace_data.steps.length - 1 && (
                                    <div className="step-connector">↓</div>
                                )}
                            </div>
                        )
                    })}
                </div>
            </div>
        </section>
    )
}

export default TraceDetail