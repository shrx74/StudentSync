import { FaExclamationTriangle } from 'react-icons/fa'

function ConflictBanner({ message }) {
  return (
    <div className="banner">
      <div className="banner-title">
        <FaExclamationTriangle /> Scheduling conflict
      </div>
      <div>{message}</div>
    </div>
  )
}

export default ConflictBanner
