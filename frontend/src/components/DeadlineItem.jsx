function DeadlineItem({ title, date, status, amount }) {
  return (
    <div className="item">
      <div>
        <div className="item-title">{title}</div>
        <div className="item-small">{date}</div>
      </div>
      {status && <span className="status">{status}</span>}
      {amount && <span className="amount">{amount}</span>}
    </div>
  )
}

export default DeadlineItem
