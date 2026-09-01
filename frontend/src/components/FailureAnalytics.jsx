import { useEffect, useState } from "react"

const CLASSIFIER_METRICS = {
    infinite_loop: {
        precision: 1.0,
        recall: 1.0,
        f1: 1.0
    },
    retry_storm: {
        precision: 1.0,
        recall: 1.0,
        f1: 1.0
    },
    tool_misuse: {
        precision: 1.0,
        recall: 1.0,
        f1: 1.0
    },
    context_overflow: {
        precision: 1.0,
        recall: 1.0,
        f1: 1.0
    },
    prompt_injection: {
        precision: 1.0,
        recall: 1.0,
        f1: 1.0
    },
    hallucination: {
        precision: 1.0,
        recall: 0.76,
        f1: 0.8636363636363636
    },
    intent_drift: {
        precision: 0.7936507936507936,
        recall: 1.0,
        f1: 0.8849557522123894
    }
}

function FailureAnalytics() {
    const [stats, setStats] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    useEffect(() => {
        fetch("http://127.0.0.1:8000/stats")
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Failed to fetch analytics")
                }

                return response.json()
            })
            .then((data) => {
                setStats(data)
            })
            .catch((error) => {
                console.error(error)
                setError("Failed to load analytics.")
            })
            .finally(() => {
                setLoading(false)
            })
    }, [])

    if (loading) {
        return <p>Loading analytics...</p>
    }

    if (error) {
        return <p>{error}</p>
    }

    const totalTraces = stats?.total_traces ?? 0

    const failures =
        totalTraces -
        (stats?.failure_count?.none ?? 0) -
        (stats?.failure_count?.unclassified ?? 0)

    const failureRate =
        totalTraces > 0
            ? ((failures / totalTraces) * 100).toFixed(1)
            : 0

    const failureCounts = stats?.failure_count ?? {}

    const failureModes = [
        "infinite_loop",
        "retry_storm",
        "tool_misuse",
        "context_overflow",
        "prompt_injection",
        "hallucination",
        "intent_drift"
    ]

    const maxFailureCount = Math.max(
        ...failureModes.map((mode) => failureCounts[mode] ?? 0),
        1
    )

    return (
        <section className="failure-analytics">
            <div className="section-header">
                <h2>Failure Analytics</h2>
                <p>Analyze detected AI agent failures.</p>
            </div>

            <div className="analytics-stats">
                <div className="analytics-card">
                    <h3>Total Traces</h3>
                    <strong>{totalTraces}</strong>
                </div>

                <div className="analytics-card">
                    <h3>Total Failures</h3>
                    <strong>{failures}</strong>
                </div>

                <div className="analytics-card">
                    <h3>Failure Rate</h3>
                    <strong>{failureRate}%</strong>
                </div>
            </div>

            <div className="failure-distribution">
                <div className="section-header">
                    <h2>Failure Distribution</h2>
                    <p>Number of traces detected for each failure mode.</p>
                </div>

                <div className="failure-bars">
                    {failureModes.map((mode) => {
                        const count = failureCounts[mode] ?? 0
                        const width = (count / maxFailureCount) * 100

                        return (
                            <div className="failure-bar-row" key={mode}>
                                <span className="failure-label">
                                    {mode.replaceAll("_", " ")}
                                </span>

                                <div className="failure-bar-track">
                                    <div
                                        className="failure-bar"
                                        style={{ width: `${width}%` }}
                                    />
                                </div>

                                <span className="failure-count">
                                    {count}
                                </span>
                            </div>
                        )
                    })}
                </div>
            </div>

            <div className="classifier-performance">
                <div className="section-header">
                    <h2>Classifier Performance</h2>
                    <p>
                        Precision, recall, and F1 measured on the synthetic benchmark.
                    </p>
                </div>

                <div className="metrics-table">
                    <div className="metrics-row metrics-header">
                        <span>Failure Mode</span>
                        <span>Precision</span>
                        <span>Recall</span>
                        <span>F1</span>
                    </div>

                    {Object.entries(CLASSIFIER_METRICS).map(([mode, metrics]) => (
                        <div className="metrics-row" key={mode}>
                            <span>
                                {mode.replaceAll("_", " ")}
                            </span>

                            <span>
                                {(metrics.precision * 100).toFixed(2)}%
                            </span>

                            <span>
                                {(metrics.recall * 100).toFixed(2)}%
                            </span>

                            <span>
                                {(metrics.f1 * 100).toFixed(2)}%
                            </span>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    )
}

export default FailureAnalytics