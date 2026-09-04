function Sidebar() {
    return (
        <aside className="sidebar">
            <div className="sidebar-brand">
                <h1>Vigil</h1>
                <p>AI Agent Observability</p>
            </div>

            <nav>
                <a href="#overview">Dashboard</a>
                <a href="#traces">Traces</a>
                <a href="#failures">Failures</a>
                <a href="#analytics">Analytics</a>
            </nav>
        </aside>
    )
}

export default Sidebar