import { useState } from 'react'
import Footer from './components/Footer'
import Header from './components/Header'
import DashboardPage from './pages/DashboardPage'
import AcademicsPage from './pages/AcademicsPage'
import WorkPage from './pages/WorkPage'

function App() {
  const [page, setPage] = useState('Dashboard')

  return (
    <div className="page">
      <Header page={page} onNavigate={setPage} />
      <main className="dashboard">
        {page === 'Dashboard' && <DashboardPage />}
        {page === 'Academics' && <AcademicsPage />}
        {page === 'Work' && <WorkPage />}
      </main>
      <Footer />
    </div>
  )
}

export default App
