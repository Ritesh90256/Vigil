import StatCard from "./StatCard"
import RecentTraces from "./RecentTraces"

function Dashboard() {
    const traces = [
        {
            goal: "Find the weather in a city",
            failure: "None",
            confidence: "High",
        },
        {
            goal: "Schedule a meeting",
            failure: "Tool Misuse",
            confidence: "High",
        },
        {
            goal: "Search for AI news",
            failure: "Hallucination",
            confidence: "Medium",
        },
        ]
    return (
        <section className="dashboard">
            <div className="dashboard-header">
              <h1>Overview</h1>
              <p>Monitor AI agent activity and failures.</p>
            </div>

            <div className="stats">
                <StatCard title="Total Traces" value="767" />
                <StatCard title="Failures" value="106" />
                <StatCard title="Failure Rate" value="13.8%" />
            </div>

            <RecentTraces traces = {traces} />

          </section>
    )
}

export default Dashboard