import { IoWalletOutline } from 'react-icons/io5'
import FinanceTile from './FinanceTile'

function FinancialOverview() {
  return (
    <section className="panel">
      <h2><IoWalletOutline /> Financial Overview</h2>
      <div className="tiles">
        <FinanceTile label="Estimated vs. actual earnings" value="$850.00 / $820.00" />
        <FinanceTile label="Income vs. expenses" value="$820.00 / $540.00" />
        <FinanceTile label="Budget remaining this month" value="$260.00" />
        <FinanceTile label="Savings target" value="$400.00 / $1,000.00" progress={40} />
      </div>
    </section>
  )
}

export default FinancialOverview
