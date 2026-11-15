function ScheduleItem({ time, title, type, isConflict }) {
  return (
    <div className="item">
      <div className="item-time">{time}</div>
      <div>
        <div className="item-title">{title}</div>
        <div className="item-small">{type}</div>
      </div>
      {isConflict && <span className="conflict">Conflict</span>}
    </div>
  )
}

export default ScheduleItem
