import { useEffect, useState } from "react"

const API_URL = "http://127.0.0.1:8000"

function TraceExplorer() {
  const [failureMode, setFailureMode] = useState("")
  const [confidence, setConfidence] = useState("")
  const [page, setPage] = useState(1)
  const [traces, setTraces] = useState([])
  const [hasNextPage, setHasNextPage] = useState(true)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    setLoading(true)
    setError(null)

    let url = `${API_URL}/traces?page=${page}&limit=20`

    if (failureMode) {
      url += `&failure_mode=${failureMode}`
    }

    if (confidence) {
      url += `&confidence=${confidence}`
    }

    fetch(url)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch traces")
        }

        return response.json()
      })
      .then((data) => {
        setTraces(data)
        setHasNextPage(data.length === 20)
      })
      .catch((error) => {
        console.error(error)
        setError("Failed to load traces.")
        setTraces([])
        setHasNextPage(false)
      })
      .finally(() => {
        setLoading(false)
      })
  }, [failureMode, confidence, page])

  if (error) {
    return <p>{error}</p>
  }

  return (
    <div className="recent-traces">
      <div className="section-header">
        <h2>Recent Traces</h2>
        <p>Latest AI agent executions.</p>
      </div>

      <div className="filters">
        <label htmlFor="failure-mode">Failure Mode</label>

        <select
          id="failure-mode"
          value={failureMode}
          onChange={(event) => {
            setFailureMode(event.target.value)
            setPage(1)
            setHasNextPage(true)
          }}
        >
          <option value="">All</option>
          <option value="none">None</option>
          <option value="infinite_loop">Infinite Loop</option>
          <option value="retry_storm">Retry Storm</option>
          <option value="tool_misuse">Tool Misuse</option>
          <option value="context_overflow">Context Overflow</option>
          <option value="prompt_injection">Prompt Injection</option>
          <option value="hallucination">Hallucination</option>
          <option value="intent_drift">Intent Drift</option>
        </select>

        <label htmlFor="confidence">Confidence</label>

        <select
          id="confidence"
          value={confidence}
          onChange={(event) => {
            setConfidence(event.target.value)
            setPage(1)
            setHasNextPage(true)
          }}
        >
          <option value="">All</option>
          <option value="high">High</option>
          <option value="medium">Medium</option>
          <option value="low">Low</option>
        </select>
      </div>

      {loading ? (
        <p>Loading traces...</p>
      ) : traces.length === 0 ? (
        <p>No traces found.</p>
      ) : (
        <div className="trace-table">
          <div className="trace-row trace-header">
            <span>Agent Goal</span>
            <span>Failure Mode</span>
            <span>Confidence</span>
          </div>

          {traces.map((trace) => (
            <div className="trace-row" key={trace.id}>
              <span>{trace.agent_goal}</span>
              <span>{trace.failure_mode}</span>
              <span>{trace.confidence}</span>
            </div>
          ))}
        </div>
      )}

      {!loading && traces.length > 0 && (
        <div className="pagination">
          <button
            onClick={() => setPage(page - 1)}
            disabled={page === 1}
          >
            Previous
          </button>

          <span>Page {page}</span>

          <button
            onClick={() => setPage(page + 1)}
            disabled={!hasNextPage}
          >
            Next
          </button>
        </div>
      )}
    </div>
  )
}

export default TraceExplorer