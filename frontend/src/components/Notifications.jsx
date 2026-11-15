import { FaRegBell } from 'react-icons/fa'
import NotificationItem from './NotificationItem'

function Notifications() {
    return (
        <section className="panel">
            <h2><FaRegBell /> Notifications</h2>
            <div className="items">
                <NotificationItem type="conflict" title="Scheduling conflict" message="Calculus Review overlaps with Campus Library Desk, 02:00 - 03:30 PM" />
                <NotificationItem type="reminder" title="Due within 48 hours" message="Programming Assignment 1 - 2026-09-20, 11:59 PM" />
            </div>
        </section>
    )
}

export default Notifications
