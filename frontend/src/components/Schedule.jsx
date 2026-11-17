import { FaRegCalendarAlt } from 'react-icons/fa'
import ScheduleItem from './ScheduleItem'

function Schedule({ date, items }) {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2><FaRegCalendarAlt /> Schedule</h2>
        <span className="item-small">{date}</span>
      </div>
      <div className="items">
        {items.map((item) => (
          <ScheduleItem
            key={item.id}
            time={item.time}
            title={item.title}
            type={item.type}
            isConflict={item.isConflict}
          />
        ))}
      </div>
    </section>
  )
}

export default Schedule
