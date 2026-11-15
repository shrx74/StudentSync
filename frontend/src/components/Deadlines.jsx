import { FaRegClock } from 'react-icons/fa'
import DeadlineItem from './DeadlineItem'

function Deadlines() {
  return (
    <section className="panel">
      <h2><FaRegClock /> Upcoming Deadlines &amp; Costs</h2>
      <div className="items">
        <DeadlineItem title="Programming Assignment 1" date="2026-09-20, 11:59 PM" status="In Progress" />
        <DeadlineItem title="Rent" date="2026-10-01" amount="$600.00" />
      </div>
    </section>
  )
}

export default Deadlines
