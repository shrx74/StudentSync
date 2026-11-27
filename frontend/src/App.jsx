import { useEffect, useState } from 'react'
import Footer from './components/Footer'
import Header from './components/Header'
import Schedule from './components/Schedule'
import Notifications from './components/Notifications'
import Deadlines from './components/Deadlines'
import ConflictBanner from './components/ConflictBanner'
import FinancialOverview from './components/FinancialOverview'
import { toDashboard } from './dashboard'

const USER_ID = 1

function App() {
  const [dashboard, setDashboard] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    fetch(`/users/${USER_ID}/dashboard`)
      .then((response) => {
        if (!response.ok) {
          throw new Error('Could not load the dashboard')
        }
        return response.json()
      })
      .then((data) => setDashboard(toDashboard(data)))
      .catch((err) => setError(err.message))
  }, [])

  return (
    <div className="page">
      <Header />
      <main className="dashboard">
        <h1>Dashboard</h1>
        {error && <p>{error}</p>}
        {!dashboard && !error && <p>Loading...</p>}
        {dashboard && (
          <>
            {dashboard.conflictMessage && <ConflictBanner message={dashboard.conflictMessage} />}
            <div className="panels">
              <Schedule date={dashboard.date} items={dashboard.schedule} />
              <Notifications items={dashboard.notifications} />
              <Deadlines items={dashboard.deadlines} />
              <FinancialOverview tiles={dashboard.finance} />
            </div>
          </>
        )}
      </main>
      <Footer />
    </div>
  )
}

export default App
