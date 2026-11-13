
-- 1. Users: Stores student account information.
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    timezone VARCHAR(50) DEFAULT 'UTC',
    currency VARCHAR(3) DEFAULT 'CAD',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Semesters: Stores academic semester information.
CREATE TABLE IF NOT EXISTS semesters (
    semester_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    semester_name VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    CHECK (end_date >= start_date)
);

-- 3. Courses: Stores courses taken during a semester.
CREATE TABLE IF NOT EXISTS courses (
    course_id SERIAL PRIMARY KEY,
    semester_id INT NOT NULL REFERENCES semesters(semester_id) ON DELETE CASCADE,
    course_code VARCHAR(30) NOT NULL,
    course_name VARCHAR(150) NOT NULL,
    instructor VARCHAR(100),
    location VARCHAR(150)
);

-- 4. Class Meetings: Stores weekly class schedules.
CREATE TABLE IF NOT EXISTS class_meetings (
    meeting_id SERIAL PRIMARY KEY,
    course_id INT NOT NULL REFERENCES courses(course_id) ON DELETE CASCADE,
    day_of_week INT NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    location VARCHAR(150),
    CHECK (day_of_week BETWEEN 1 AND 7),
    CHECK (end_time > start_time),
    CHECK (end_date >= start_date)
);

-- 5. Academic Tasks: Stores assignments, projects, quizzes and exams.
CREATE TABLE IF NOT EXISTS academic_tasks (
    task_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    course_id INT REFERENCES courses(course_id) ON DELETE SET NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    task_type VARCHAR(30) DEFAULT 'assignment',
    due_date TIMESTAMPTZ NOT NULL,
    status VARCHAR(30) DEFAULT 'pending'
);

-- 6. Study Sessions: Stores planned study schedules.
CREATE TABLE IF NOT EXISTS study_sessions (
    session_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    course_id INT REFERENCES courses(course_id) ON DELETE SET NULL,
    title VARCHAR(150) NOT NULL,
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ NOT NULL,
    notes TEXT,
    CHECK (end_time > start_time)
);

-- 7. Activities: Stores personal activities and events.
CREATE TABLE IF NOT EXISTS activities (
    activity_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    location VARCHAR(150),
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ NOT NULL,
    CHECK (end_time > start_time)
);

-- 8. Jobs: Stores student employment information.
CREATE TABLE IF NOT EXISTS jobs (
    job_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    employer VARCHAR(150) NOT NULL,
    job_title VARCHAR(100),
    hourly_wage NUMERIC(10,2) NOT NULL,
    start_date DATE,
    end_date DATE,
    CHECK (hourly_wage >= 0)
);

-- 9. Work Shifts: Stores working hours and breaks.
CREATE TABLE IF NOT EXISTS work_shifts (
    shift_id SERIAL PRIMARY KEY,
    job_id INT NOT NULL REFERENCES jobs(job_id) ON DELETE CASCADE,
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ NOT NULL,
    break_minutes INT DEFAULT 0,
    break_paid BOOLEAN DEFAULT FALSE,
    notes TEXT,
    CHECK (end_time > start_time),
    CHECK (break_minutes >= 0)
);

-- 10. Income Records: Stores student income information.
CREATE TABLE IF NOT EXISTS income_records (
    income_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    job_id INT REFERENCES jobs(job_id) ON DELETE SET NULL,
    source VARCHAR(150) NOT NULL,
    amount NUMERIC(10,2) NOT NULL,
    income_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'actual',
    notes TEXT,
    CHECK (amount > 0)
);

-- 11. Expense Categories: Stores expense category names.
CREATE TABLE IF NOT EXISTS expense_categories (
    category_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    category_name VARCHAR(100) NOT NULL,
    UNIQUE (user_id, category_name)
);

-- 12. Expense Records: Stores individual expenses.
CREATE TABLE IF NOT EXISTS expense_records (
    expense_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    category_id INT NOT NULL REFERENCES expense_categories(category_id),
    description VARCHAR(200) NOT NULL,
    amount NUMERIC(10,2) NOT NULL,
    expense_date DATE NOT NULL,
    notes TEXT,
    CHECK (amount > 0)
);

-- 13. Budgets: Stores spending limits for selected periods.
CREATE TABLE IF NOT EXISTS budgets (
    budget_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    budget_name VARCHAR(100) NOT NULL,
    spending_limit NUMERIC(10,2) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    CHECK (spending_limit >= 0),
    CHECK (end_date >= start_date)
);

-- 14. Savings Targets: Stores student savings goals.
CREATE TABLE IF NOT EXISTS savings_targets (
    target_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    target_name VARCHAR(150) NOT NULL,
    target_amount NUMERIC(10,2) NOT NULL,
    target_date DATE,
    CHECK (target_amount > 0)
);

-- 15. Savings Contributions: Stores money saved toward a goal.
CREATE TABLE IF NOT EXISTS savings_contributions (
    contribution_id SERIAL PRIMARY KEY,
    target_id INT NOT NULL REFERENCES savings_targets(target_id) ON DELETE CASCADE,
    amount NUMERIC(10,2) NOT NULL,
    contribution_date DATE NOT NULL,
    notes TEXT,
    CHECK (amount > 0)
);

-- 16. Reminders: Stores reminders for upcoming events.
CREATE TABLE IF NOT EXISTS reminders (
    reminder_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    task_id INT REFERENCES academic_tasks(task_id) ON DELETE CASCADE,
    shift_id INT REFERENCES work_shifts(shift_id) ON DELETE CASCADE,
    session_id INT REFERENCES study_sessions(session_id) ON DELETE CASCADE,
    activity_id INT REFERENCES activities(activity_id) ON DELETE CASCADE,
    remind_at TIMESTAMPTZ NOT NULL,
    status VARCHAR(20) DEFAULT 'pending'
);
