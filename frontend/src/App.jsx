import Footer from './components/Footer'
import Header from './components/Header'
import Schedule from './components/Schedule'
import Notifications from './components/Notifications'
import Deadlines from './components/Deadlines'
import ConflictBanner from './components/ConflictBanner'
import FinancialOverview from './components/FinancialOverview'
import { dashboardData } from './sampleData'

function App() {
  return (
    <div className="page">
      <Header />
      <main className="dashboard">
        <h1>Dashboard</h1>
        {dashboardData.hasConflict && <ConflictBanner message={dashboardData.conflictMessage} />}
        <div className="panels">
          <Schedule date={dashboardData.date} items={dashboardData.schedule} />
          <Notifications items={dashboardData.notifications} />
          <Deadlines items={dashboardData.deadlines} />
          <FinancialOverview tiles={dashboardData.finance} />
        </div>
      </main>
      <Footer />
    </div>
  )
}

export default App
