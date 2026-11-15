import { FaRegCalendarAlt } from 'react-icons/fa'
import ScheduleItem from './ScheduleItem'

function Schedule() {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2><FaRegCalendarAlt /> Schedule</h2>
        <span className="item-small">Friday, 2026-09-18</span>
      </div>
      <div className="items">
        <ScheduleItem time="09:00 – 10:30 AM" title="Introduction to Computer Science" type="Class" />
        <ScheduleItem time="01:00 – 05:30 PM" title="Campus Library Desk" type="Work Shift" isConflict={true} />
        <ScheduleItem time="02:00 – 03:30 PM" title="Calculus Review" type="Study Session" isConflict={true} />
      </div>
    </section>
  )
}

export default Schedule
