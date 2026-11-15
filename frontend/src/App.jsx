import Footer from './components/Footer'
import Header from './components/Header'
import Schedule from './components/Schedule'
import Notifications from './components/Notifications'
import Deadlines from './components/Deadlines'
import ConflictBanner from './components/ConflictBanner'
import FinancialOverview from './components/FinancialOverview'

function App() {
  const hasConflict = true

  return (
    <div className="page">
      <Header />
      <main className="dashboard">
        <h1>Dashboard</h1>
        {hasConflict && <ConflictBanner />}
        <div className="panels">
          <Schedule />
          <Notifications />
          <Deadlines />
          <FinancialOverview />
        </div>
      </main>
      <Footer />
    </div>
  )
}

export default App
