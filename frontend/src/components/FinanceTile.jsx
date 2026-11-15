function FinanceTile({ label, value, progress }) {
  return (
    <div className="tile">
      <div className="item-small">{label}</div>
      <div className="tile-value">{value}</div>
      {progress !== undefined && (
        <div className="progress-track">
          <div className="progress-fill" style={{ width: `${progress}%` }}></div>
        </div>
      )}
    </div>
  )
}

export default FinanceTile
