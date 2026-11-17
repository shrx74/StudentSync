import { FaRegBell } from 'react-icons/fa'
import NotificationItem from './NotificationItem'

function Notifications({ items }) {
  return (
    <section className="panel">
      <h2><FaRegBell /> Notifications</h2>
      <div className="items">
        {items.map((item) => (
          <NotificationItem
            key={item.id}
            type={item.type}
            title={item.title}
            message={item.message}
          />
        ))}
      </div>
    </section>
  )
}

export default Notifications
