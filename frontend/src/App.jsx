import './App.css'

function App() {
  return (
    <div className="app">
      <aside className="sidebar">
        <h1>Vigil</h1>
        <nav>
          <a href="#">Dashboard</a>
          <a href="#">Traces</a>
          <a href="#">Failures</a>
          <a href="#">Analytics</a>
        </nav>
      </aside>

      <div className="content">
        <header className="header">
          <h2>Dashboard</h2>
        </header>

        <main className="main">
          <section className="dashboard">
            <div className="dashboard-header">
              <h1>Overview</h1>
              <p>Monitor AI agent activity and failures.</p>
            </div>

            <div className="stats">
              <article className="stat-card">
                <h3>Total Traces</h3>
                <strong>767</strong>
              </article>

              <article className="stat-card">
                <h3>Failures</h3>
                <strong>106</strong>
              </article>

              <article className="stat-card">
                <h3>Failure Rate</h3>
                <strong>13.8%</strong>
              </article>
            </div>

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

                <div className="trace-row">
                  <span>Find the weather in a city</span>
                  <span>None</span>
                  <span>High</span>
                </div>

                <div className="trace-row">
                  <span>Schedule a meeting</span>
                  <span>Tool Misuse</span>
                  <span>High</span>
                </div>

                <div className="trace-row">
                  <span>Search for AI news</span>
                  <span>Retry Storm</span>
                  <span>Medium</span>
                </div>
              </div>
            </div>
            
          </section>
        </main>
      </div>
    </div>
  )
}

export default App
 