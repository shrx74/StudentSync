import { useEffect, useState } from 'react'
import { FaBriefcase, FaPlus, FaRegCalendarAlt } from 'react-icons/fa'
import { request } from '../api'
import { clockTime, dateTime, money } from '../format'

const EMPTY_JOB = { employer: '', hourly_wage: '' }
const EMPTY_SHIFT = { job_id: '', start_time: '', end_time: '', break_minutes: '0', break_paid: false }

function toUtc(value) {
  return value && new Date(value).toISOString()
}

function WorkPage() {
  const [jobs, setJobs] = useState([])
  const [shifts, setShifts] = useState([])
  const [jobForm, setJobForm] = useState(EMPTY_JOB)
  const [shiftForm, setShiftForm] = useState(EMPTY_SHIFT)
  const [jobError, setJobError] = useState('')
  const [shiftError, setShiftError] = useState('')

  function loadWork() {
    request('/jobs').then(setJobs).catch((err) => setJobError(err.message))
    request('/shifts').then(setShifts).catch((err) => setShiftError(err.message))
  }

  useEffect(loadWork, [])

  function handleJobChange(event) {
    setJobForm({ ...jobForm, [event.target.name]: event.target.value })
  }

  function handleShiftChange(event) {
    const { name, type, value, checked } = event.target
    setShiftForm({ ...shiftForm, [name]: type === 'checkbox' ? checked : value })
  }

  function handleJobSubmit(event) {
    event.preventDefault()
    setJobError('')

    request('/jobs', { method: 'POST', body: JSON.stringify(jobForm) })
      .then(() => {
        setJobForm(EMPTY_JOB)
        loadWork()
      })
      .catch((err) => setJobError(err.message))
  }

  function handleShiftSubmit(event) {
    event.preventDefault()
    setShiftError('')

    const shift = {
      job_id: shiftForm.job_id ? Number(shiftForm.job_id) : '',
      start_time: toUtc(shiftForm.start_time),
      end_time: toUtc(shiftForm.end_time),
      break_minutes: Number(shiftForm.break_minutes || 0),
      break_paid: shiftForm.break_paid,
    }

    request('/shifts', { method: 'POST', body: JSON.stringify(shift) })
      .then(() => {
        setShiftForm(EMPTY_SHIFT)
        loadWork()
      })
      .catch((err) => setShiftError(err.message))
  }

  function handleDeleteShift(shiftId) {
    request(`/shifts/${shiftId}`, { method: 'DELETE' })
      .then(loadWork)
      .catch((err) => setShiftError(err.message))
  }

  return (
    <>
      <h1>Work</h1>
      <div className="panels">
        <section className="panel">
          <h2><FaPlus /> Add a Shift</h2>
          <form className="form" onSubmit={handleShiftSubmit}>
            <label>
              Job
              <select name="job_id" value={shiftForm.job_id} onChange={handleShiftChange}>
                <option value="">Choose a job</option>
                {jobs.map((job) => (
                  <option key={job.job_id} value={job.job_id}>{job.employer}</option>
                ))}
              </select>
            </label>
            <label>
              Start
              <input type="datetime-local" name="start_time" value={shiftForm.start_time} onChange={handleShiftChange} />
            </label>
            <label>
              End
              <input type="datetime-local" name="end_time" value={shiftForm.end_time} onChange={handleShiftChange} />
            </label>
            <label>
              Break (minutes)
              <input type="number" min="0" name="break_minutes" value={shiftForm.break_minutes} onChange={handleShiftChange} />
            </label>
            <label className="checkbox">
              <input type="checkbox" name="break_paid" checked={shiftForm.break_paid} onChange={handleShiftChange} />
              Paid break
            </label>
            {shiftError && <p className="error">{shiftError}</p>}
            <button type="submit" className="button">Add shift</button>
          </form>
        </section>

        <section className="panel">
          <h2><FaRegCalendarAlt /> Shifts</h2>
          <div className="items">
            {shifts.length === 0 && <p className="empty">No shifts yet.</p>}
            {shifts.map((shift) => (
              <div className="item" key={shift.shift_id}>
                <div>
                  <div className="item-title">{shift.employer}</div>
                  <div className="item-small">
                    {dateTime(shift.start_time)} – {clockTime(shift.end_time)} · {money(shift.estimated_earnings)}
                  </div>
                </div>
                <button type="button" className="link-button" onClick={() => handleDeleteShift(shift.shift_id)}>
                  Delete
                </button>
              </div>
            ))}
          </div>
        </section>

        <section className="panel">
          <h2><FaPlus /> Add a Job</h2>
          <form className="form" onSubmit={handleJobSubmit}>
            <label>
              Employer
              <input name="employer" value={jobForm.employer} onChange={handleJobChange} />
            </label>
            <label>
              Hourly wage ($)
              <input type="number" min="0" step="0.01" name="hourly_wage" value={jobForm.hourly_wage} onChange={handleJobChange} />
            </label>
            {jobError && <p className="error">{jobError}</p>}
            <button type="submit" className="button">Add job</button>
          </form>
        </section>

        <section className="panel">
          <h2><FaBriefcase /> Jobs</h2>
          <div className="items">
            {jobs.length === 0 && <p className="empty">No jobs yet.</p>}
            {jobs.map((job) => (
              <div className="item" key={job.job_id}>
                <div className="item-title">{job.employer}</div>
                <span className="amount">{money(job.hourly_wage)}/h</span>
              </div>
            ))}
          </div>
        </section>
      </div>
    </>
  )
}

export default WorkPage
