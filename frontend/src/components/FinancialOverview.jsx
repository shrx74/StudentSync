import { IoWalletOutline } from 'react-icons/io5'
import FinanceTile from './FinanceTile'

function FinancialOverview({ tiles }) {
  return (
    <section className="panel">
      <h2><IoWalletOutline /> Financial Overview</h2>
      <div className="tiles">
        {tiles.map((tile) => (
          <FinanceTile
            key={tile.id}
            label={tile.label}
            value={tile.value}
            progress={tile.progress}
          />
        ))}
      </div>
    </section>
  )
}

export default FinancialOverview
