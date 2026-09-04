import { useEffect, useState } from "react"
import StatCard from "./StatCard"
import TraceExplorer from "./TraceExplorer"
import TraceDetail from "./TraceDetail"
import FailureAnalytics from "./FailureAnalytics"

const API_URL = "http://127.0.0.1:8000"

function Dashboard() {
    const [stats, setStats] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)
    const [selectedTraceId, setSelectedTraceId] = useState(null)

    useEffect(() => {
        Promise.all([
            fetch(`${API_URL}/stats`)
        ])
            .then(([statsResponse]) => {
                if (!statsResponse.ok) {
                    throw new Error("Failed to fetch dashboard data")
                }

                return statsResponse.json()
            })
            .then((statsData) => {
                setStats(statsData)
            })
            .catch((error) => {
                console.error(error)
                setError("Failed to load dashboard data.")
            })
            .finally(() => {
                setLoading(false)
            })
    }, [])

    const totalTraces = stats?.total_traces ?? 0

    const failures =
        totalTraces -
        (stats?.failure_count?.none ?? 0) -
        (stats?.failure_count?.unclassified ?? 0)

    const failureRate =
        totalTraces > 0
            ? ((failures / totalTraces) * 100).toFixed(1)
            : 0

    if (error) {
        return <p className="status-message">{error}</p>
    }

    return (
        <section className="dashboard">
            <div className="dashboard-header" id="overview">
                <h1>Overview</h1>
                <p>Monitor AI agent activity, execution health, and detected failures.</p>
            </div>

            <div className="stats">
                <StatCard
                    title="Total Traces"
                    value={loading ? "..." : totalTraces}
                />

                <StatCard
                    title="Failures"
                    value={loading ? "..." : failures}
                />

                <StatCard
                    title="Failure Rate"
                    value={loading ? "..." : `${failureRate}%`}
                />
            </div>

            <TraceExplorer onTraceSelect={setSelectedTraceId} />

            {selectedTraceId && <TraceDetail traceId={selectedTraceId} />}

            <FailureAnalytics />
        </section>
    )
}

export default Dashboard