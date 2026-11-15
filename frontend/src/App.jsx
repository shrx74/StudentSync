import Footer from './components/Footer'
import Header from './components/Header'
import Schedule from './components/Schedule'

function App() {
  return (
    <div className="page">
      <Header/>
      <main className="dashboard">
        <h1>Dashboard</h1>
        <div className="panels">
          <Schedule/>
        </div>
      </main>
      <Footer/>
    </div>
  )
}

export default App
