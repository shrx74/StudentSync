import { FaRegClock } from 'react-icons/fa'
import DeadlineItem from './DeadlineItem'

function Deadlines({ items }) {
  return (
    <section className="panel">
      <h2><FaRegClock /> Upcoming Deadlines & Costs</h2>
      <div className="items">
        {items.map((item) => (
          <DeadlineItem
            key={item.id}
            title={item.title}
            date={item.date}
            status={item.status}
            amount={item.amount}
          />
        ))}
      </div>
    </section>
  )
}

export default Deadlines
