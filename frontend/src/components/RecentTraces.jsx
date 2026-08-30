function RecentTraces({traces}) {
  return (
    <div className="recent-traces">
      <div className="section-header">
        <h2>Recent Traces</h2>
        <p>Latest AI agent executions.</p>
      </div>

      <div className="trace-table">
        <div className="trace-row trace-header">
          <span>Agent Goal</span>
          <span>Failure Mode</span>
          <span>Confidence</span>
        </div>

        {traces.map((trace) => (
          <div className="trace-row" key={trace.goal}>
            <span>{trace.goal}</span>
            <span>{trace.failure}</span>
            <span>{trace.confidence}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

export default RecentTraces