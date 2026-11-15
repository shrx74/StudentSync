export const dashboardData = {
    hasConflict: true,
    conflictMessage: '"Study Session (Calculus Review)" overlaps with "Work Shift (Campus Library Desk)" on 2026-09-18 from 02:00 PM to 03:30 PM.',
    date: 'Friday, 2026-09-18',
    schedule: [
        { id: 1, time: '09:00 – 10:30 AM', title: 'Introduction to Computer Science', type: 'Class', isConflict: false },
        { id: 2, time: '01:00 – 05:30 PM', title: 'Campus Library Desk', type: 'Work Shift', isConflict: true },
        { id: 3, time: '02:00 – 03:30 PM', title: 'Calculus Review', type: 'Study Session', isConflict: true },
    ],
    notifications: [
        { id: 1, type: 'conflict', title: 'Scheduling conflict', message: 'Calculus Review overlaps with Campus Library Desk, 02:00 – 03:30 PM' },
        { id: 2, type: 'reminder', title: 'Due within 48 hours', message: 'Programming Assignment 1 · 2026-09-20, 11:59 PM' },
    ],
    deadlines: [
        { id: 1, title: 'Programming Assignment 1', date: '2026-09-20, 11:59 PM', status: 'In Progress' },
        { id: 2, title: 'Rent', date: '2026-10-01', amount: '$600.00' },
    ],
    finance: [
        { id: 1, label: 'Estimated vs. actual earnings', value: '$850.00 / $820.00' },
        { id: 2, label: 'Income vs. expenses', value: '$820.00 / $540.00' },
        { id: 3, label: 'Budget remaining this month', value: '$260.00' },
        { id: 4, label: 'Savings target', value: '$750.00 / $1,000.00', progress: (750 / 1000) * 100 },
    ],
}