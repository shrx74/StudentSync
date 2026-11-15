import { FaExclamationTriangle } from 'react-icons/fa'

function ConflictBanner() {
  return (
    <div className="banner">
      <div className="banner-title">
        <FaExclamationTriangle /> Scheduling conflict
      </div>
      <div>"Study Session (Calculus Review)" overlaps with "Work Shift (Campus Library Desk)" on 2026-09-18 from 02:00 PM to 03:30 PM.</div>
    </div>
  )
}

export default ConflictBanner
