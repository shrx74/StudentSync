import { useEffect, useState } from 'react'
import { FaRegClock, FaPlus } from 'react-icons/fa'
import { request } from '../api'
import { dateTime } from '../format'

const TASK_TYPES = ['assignment', 'project', 'quiz', 'exam', 'other']
const EMPTY_TASK = { title: '', due_date: '', task_type: 'assignment' }

function AcademicsPage() {
  const [tasks, setTasks] = useState([])
  const [form, setForm] = useState(EMPTY_TASK)
  const [error, setError] = useState('')

  function loadTasks() {
    request('/tasks')
      .then(setTasks)
      .catch((err) => setError(err.message))
  }

  useEffect(loadTasks, [])

  function handleChange(event) {
    setForm({ ...form, [event.target.name]: event.target.value })
  }

  function handleSubmit(event) {
    event.preventDefault()
    setError('')

    const task = { ...form, due_date: form.due_date && new Date(form.due_date).toISOString() }

    request('/tasks', { method: 'POST', body: JSON.stringify(task) })
      .then(() => {
        setForm(EMPTY_TASK)
        loadTasks()
      })
      .catch((err) => setError(err.message))
  }

  function handleDelete(taskId) {
    request(`/tasks/${taskId}`, { method: 'DELETE' })
      .then(loadTasks)
      .catch((err) => setError(err.message))
  }

  return (
    <>
      <h1>Academics</h1>
      <div className="panels">
        <section className="panel">
          <h2><FaPlus /> Add a Task</h2>
          <form className="form" onSubmit={handleSubmit}>
            <label>
              Title
              <input name="title" value={form.title} onChange={handleChange} />
            </label>
            <label>
              Due date
              <input type="datetime-local" name="due_date" value={form.due_date} onChange={handleChange} />
            </label>
            <label>
              Type
              <select name="task_type" value={form.task_type} onChange={handleChange}>
                {TASK_TYPES.map((type) => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
            </label>
            {error && <p className="error">{error}</p>}
            <button type="submit" className="button">Add task</button>
          </form>
        </section>

        <section className="panel">
          <h2><FaRegClock /> Tasks</h2>
          <div className="items">
            {tasks.length === 0 && <p className="empty">No tasks yet.</p>}
            {tasks.map((task) => (
              <div className="item" key={task.task_id}>
                <div>
                  <div className="item-title">{task.title}</div>
                  <div className="item-small">{task.task_type} · {dateTime(task.due_date)}</div>
                </div>
                <button type="button" className="link-button" onClick={() => handleDelete(task.task_id)}>
                  Delete
                </button>
              </div>
            ))}
          </div>
        </section>
      </div>
    </>
  )
}

export default AcademicsPage
