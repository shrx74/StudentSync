import { useEffect, useState } from 'react'
import { FaPlus, FaPiggyBank } from 'react-icons/fa'
import { IoWalletOutline } from 'react-icons/io5'
import { request } from '../api'
import { money } from '../format'

function today() {
  return new Date().toLocaleDateString('en-CA')
}

const EMPTY_EXPENSE = { category_id: '', description: '', amount: '', expense_date: today() }
const EMPTY_INCOME = { source: '', amount: '', income_date: today() }
const EMPTY_TARGET = { target_name: '', target_amount: '' }
const EMPTY_CONTRIBUTION = { target_id: '', amount: '', contribution_date: today() }

function BudgetingPage() {
  const [finance, setFinance] = useState(null)
  const [categories, setCategories] = useState([])
  const [expense, setExpense] = useState(EMPTY_EXPENSE)
  const [income, setIncome] = useState(EMPTY_INCOME)
  const [categoryName, setCategoryName] = useState('')
  const [target, setTarget] = useState(EMPTY_TARGET)
  const [contribution, setContribution] = useState(EMPTY_CONTRIBUTION)
  const [errors, setErrors] = useState({})

  function loadBudget() {
    request('/dashboard')
      .then((data) => setFinance(data.finance))
      .catch((err) => setErrors({ list: err.message }))
    request('/expense-categories')
      .then(setCategories)
      .catch((err) => setErrors({ expense: err.message }))
  }

  useEffect(loadBudget, [])

  function update(setter, values) {
    return (event) => setter({ ...values, [event.target.name]: event.target.value })
  }

  function submit(event, key, path, body, reset) {
    event.preventDefault()
    setErrors({})

    request(path, { method: 'POST', body: JSON.stringify(body) })
      .then(() => {
        reset()
        loadBudget()
      })
      .catch((err) => setErrors({ [key]: err.message }))
  }

  function remove(path) {
    request(path, { method: 'DELETE' })
      .then(loadBudget)
      .catch((err) => setErrors({ list: err.message }))
  }

  const transactions = finance
    ? [
        ...finance.incomes.map((item) => ({
          key: `income-${item.income_id}`,
          title: item.source,
          detail: `Income · ${item.income_date}`,
          amount: `+${money(item.amount)}`,
          path: `/incomes/${item.income_id}`,
        })),
        ...finance.expenses.map((item) => ({
          key: `expense-${item.expense_id}`,
          title: item.description,
          detail: `${item.category_name} · ${item.expense_date}`,
          amount: `-${money(item.amount)}`,
          path: `/expenses/${item.expense_id}`,
        })),
      ]
    : []

  return (
    <>
      <h1>Budgeting</h1>
      <div className="panels">
        <section className="panel">
          <h2><FaPlus /> Add an Expense</h2>
          <form
            className="form"
            onSubmit={(event) => submit(
              event,
              'expense',
              '/expenses',
              { ...expense, category_id: expense.category_id ? Number(expense.category_id) : '' },
              () => setExpense(EMPTY_EXPENSE),
            )}
          >
            <label>
              Category
              <select name="category_id" value={expense.category_id} onChange={update(setExpense, expense)}>
                <option value="">Choose a category</option>
                {categories.map((category) => (
                  <option key={category.category_id} value={category.category_id}>{category.category_name}</option>
                ))}
              </select>
            </label>
            <label>
              Description
              <input name="description" value={expense.description} onChange={update(setExpense, expense)} />
            </label>
            <label>
              Amount ($)
              <input type="number" min="0" step="0.01" name="amount" value={expense.amount} onChange={update(setExpense, expense)} />
            </label>
            <label>
              Date
              <input type="date" name="expense_date" value={expense.expense_date} onChange={update(setExpense, expense)} />
            </label>
            {errors.expense && <p className="error">{errors.expense}</p>}
            <button type="submit" className="button">Add expense</button>
          </form>
          <form
            className="form inline-form"
            onSubmit={(event) => submit(event, 'category', '/expense-categories', { category_name: categoryName }, () => setCategoryName(''))}
          >
            <label>
              New category
              <input value={categoryName} onChange={(event) => setCategoryName(event.target.value)} />
            </label>
            {errors.category && <p className="error">{errors.category}</p>}
            <button type="submit" className="button">Add category</button>
          </form>
        </section>

        <section className="panel">
          <h2><FaPlus /> Add Income</h2>
          <form
            className="form"
            onSubmit={(event) => submit(event, 'income', '/incomes', income, () => setIncome(EMPTY_INCOME))}
          >
            <label>
              Source
              <input name="source" value={income.source} onChange={update(setIncome, income)} />
            </label>
            <label>
              Amount ($)
              <input type="number" min="0" step="0.01" name="amount" value={income.amount} onChange={update(setIncome, income)} />
            </label>
            <label>
              Date
              <input type="date" name="income_date" value={income.income_date} onChange={update(setIncome, income)} />
            </label>
            {errors.income && <p className="error">{errors.income}</p>}
            <button type="submit" className="button">Add income</button>
          </form>
        </section>

        <section className="panel">
          <h2><IoWalletOutline /> Transactions</h2>
          <div className="items">
            {errors.list && <p className="error">{errors.list}</p>}
            {!finance && !errors.list && <p className="empty">Loading...</p>}
            {finance && transactions.length === 0 && <p className="empty">No transactions yet.</p>}
            {transactions.map((item) => (
              <div className="item" key={item.key}>
                <div>
                  <div className="item-title">{item.title}</div>
                  <div className="item-small">{item.detail}</div>
                </div>
                <span className="amount">{item.amount}</span>
                <button type="button" className="link-button" onClick={() => remove(item.path)}>
                  Delete
                </button>
              </div>
            ))}
          </div>
        </section>

        <section className="panel">
          <h2><FaPiggyBank /> Savings</h2>
          <div className="items">
            {finance && finance.savings_targets.map((goal) => (
              <div className="tile" key={goal.target_id}>
                <div className="item-small">{goal.target_name}</div>
                <div className="tile-value">{money(goal.total_saved)} / {money(goal.target_amount)}</div>
                <div className="progress-track">
                  <div className="progress-fill" style={{ width: `${goal.percent}%` }}></div>
                </div>
              </div>
            ))}
          </div>
          <form
            className="form inline-form"
            onSubmit={(event) => submit(
              event,
              'contribution',
              `/savings-targets/${contribution.target_id}/contributions`,
              { amount: contribution.amount, contribution_date: contribution.contribution_date },
              () => setContribution(EMPTY_CONTRIBUTION),
            )}
          >
            <label>
              Add to savings
              <select name="target_id" value={contribution.target_id} onChange={update(setContribution, contribution)}>
                <option value="">Choose a goal</option>
                {finance && finance.savings_targets.map((goal) => (
                  <option key={goal.target_id} value={goal.target_id}>{goal.target_name}</option>
                ))}
              </select>
            </label>
            <label>
              Amount ($)
              <input type="number" min="0" step="0.01" name="amount" value={contribution.amount} onChange={update(setContribution, contribution)} />
            </label>
            {errors.contribution && <p className="error">{errors.contribution}</p>}
            <button type="submit" className="button" disabled={!contribution.target_id}>Add to savings</button>
          </form>
          <form
            className="form inline-form"
            onSubmit={(event) => submit(event, 'target', '/savings-targets', target, () => setTarget(EMPTY_TARGET))}
          >
            <label>
              New goal
              <input name="target_name" value={target.target_name} onChange={update(setTarget, target)} />
            </label>
            <label>
              Target amount ($)
              <input type="number" min="0" step="0.01" name="target_amount" value={target.target_amount} onChange={update(setTarget, target)} />
            </label>
            {errors.target && <p className="error">{errors.target}</p>}
            <button type="submit" className="button">Add goal</button>
          </form>
        </section>
      </div>
    </>
  )
}

export default BudgetingPage
