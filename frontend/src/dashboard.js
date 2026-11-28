import { dateTime, money } from './format'

const STATUS_LABELS = {
  pending: 'Pending',
  in_progress: 'In Progress',
  completed: 'Completed',
}

function today() {
  const date = new Date()
  const weekday = date.toLocaleDateString('en-US', { weekday: 'long' })
  return `${weekday}, ${date.toLocaleDateString('en-CA')}`
}

function conflictName(conflict) {
  return conflict.study_session || conflict.class_meeting
}

function conflictMessage(conflict) {
  return `"${conflictName(conflict)}" overlaps with "${conflict.work_shift}"`
}

function isInConflict(title, conflicts) {
  return conflicts.some(
    (conflict) => conflictName(conflict) === title || conflict.work_shift === title,
  )
}

function financeTiles(finance, schedule) {
  const earnings = schedule.reduce((sum, item) => sum + (item.estimated_earnings || 0), 0)
  const target = finance.savings_targets[0]

  const tiles = [
    { id: 1, label: 'Estimated earnings today', value: money(earnings) },
    { id: 2, label: 'Income vs. expenses', value: `${money(finance.total_income)} / ${money(finance.total_expenses)}` },
    { id: 3, label: 'Balance', value: money(finance.balance) },
  ]

  if (target) {
    tiles.push({
      id: 4,
      label: `Savings: ${target.target_name}`,
      value: `${money(target.total_saved)} / ${money(target.target_amount)}`,
      progress: target.percent,
    })
  } else {
    tiles.push({ id: 4, label: 'Savings target', value: 'No target yet' })
  }

  return tiles
}

export function toDashboard(data) {
  const conflicts = data.conflicts

  return {
    date: today(),
    conflictMessage: conflicts.length > 0 ? conflictMessage(conflicts[0]) : '',
    schedule: data.schedule.map((item, index) => ({
      id: index,
      time: `${item.start} – ${item.end}`,
      title: item.title,
      type: item.type,
      isConflict: isInConflict(item.title, conflicts),
    })),
    notifications: [
      ...conflicts.map((conflict, index) => ({
        id: `conflict-${index}`,
        type: 'conflict',
        title: 'Scheduling conflict',
        message: conflictMessage(conflict),
      })),
      ...data.reminders.map((reminder, index) => ({
        id: `reminder-${index}`,
        type: 'reminder',
        title: 'Due within 48 hours',
        message: `${reminder.title} · ${dateTime(reminder.due_date)}`,
      })),
    ],
    deadlines: data.reminders.map((reminder, index) => ({
      id: index,
      title: reminder.title,
      date: dateTime(reminder.due_date),
      status: STATUS_LABELS[reminder.status],
    })),
    finance: financeTiles(data.finance, data.schedule),
  }
}
