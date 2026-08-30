import './App.css'
import Header from './components/Header'
import Sidebar from './components/Sidebar'
import Dashboard from './components/Dashboard'

function App() {
  return (
    <div className="app">
      <Sidebar />

      <div className="content">
        <Header />

        <main className="main">
          <Dashboard />

        </main>

      </div>
      
    </div>
  )
}

export default App