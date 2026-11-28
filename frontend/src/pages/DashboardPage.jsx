import { useEffect, useState } from 'react'
import Schedule from '../components/Schedule'
import Notifications from '../components/Notifications'
import Deadlines from '../components/Deadlines'
import ConflictBanner from '../components/ConflictBanner'
import FinancialOverview from '../components/FinancialOverview'
import { request } from '../api'
import { toDashboard } from '../dashboard'

function DashboardPage() {
  const [dashboard, setDashboard] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    request('/dashboard')
      .then((data) => setDashboard(toDashboard(data)))
      .catch((err) => setError(err.message))
  }, [])

  return (
    <>
      <h1>Dashboard</h1>
      {error && <p className="error">{error}</p>}
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
    </>
  )
}

export default DashboardPage
