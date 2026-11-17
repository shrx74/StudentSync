function NotificationItem({ type, title, message }) {
  return (
    <div className="note">
      <div className={`note-title ${type}`}>{title}</div>
      <div>{message}</div>
    </div>
  )
}

export default NotificationItem
