const PAGES = ['Dashboard', 'Academics', 'Work', 'Budgeting']

function Header({ page, onNavigate }) {
  return (
    <header className="header">
      <div className="logo">Student<span className="logo-sync">Sync</span></div>
      <nav>
        {PAGES.map((name) => (
          <button
            key={name}
            type="button"
            className={name === page ? 'active' : ''}
            onClick={() => onNavigate(name)}
          >
            {name}
          </button>
        ))}
      </nav>
    </header>
  )
}

export default Header
