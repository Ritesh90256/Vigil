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
          <p>Welcome to Vigil</p>
        </main>
      </div>
    </div>
  )
}

export default App
 