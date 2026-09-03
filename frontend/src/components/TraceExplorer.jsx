import { useEffect, useState } from "react"

const API_URL = "http://127.0.0.1:8000"

function TraceExplorer({ onTraceSelect }) {
    const [failureMode, setFailureMode] = useState("")
    const [confidence, setConfidence] = useState("")
    const [page, setPage] = useState(1)
    const [traces, setTraces] = useState([])
    const [hasNextPage, setHasNextPage] = useState(true)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)
    const [search, setSearch] = useState("")
    const [debouncedSearch, setDebouncedSearch] = useState("")

    const clearFilters = () => {
        setSearch("")
        setFailureMode("")
        setConfidence("")
        setPage(1)
        setHasNextPage(true)
    }

    useEffect(() => {
        const timer = setTimeout(() => {
            setDebouncedSearch(search)
        }, 500)

        return () => {
            clearTimeout(timer)
        }
    }, [search])

    useEffect(() => {
        setLoading(true)
        setError(null)

        const params = new URLSearchParams({
            page,
            limit: 20,
        })

        if (failureMode) {
            params.set("failure_mode", failureMode)
        }

        if (confidence) {
            params.set("confidence", confidence)
        }

        if (debouncedSearch) {
            params.set("search", debouncedSearch)
        }

        const url = `${API_URL}/traces?${params.toString()}`

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
    }, [failureMode, confidence, debouncedSearch, page])

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
                <label htmlFor="search">Search</label>

                <input
                    id="search"
                    type="text"
                    placeholder="Search agent goals..."
                    value={search}
                    onChange={(event) => {
                        setSearch(event.target.value)
                        setPage(1)
                        setHasNextPage(true)
                    }}
                />

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

                <button onClick={clearFilters}>
                    Clear Filters
                </button>
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
                        <div
                            className="trace-row"
                            key={trace.id}
                            onClick={() => onTraceSelect(trace.id)}
                        >
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