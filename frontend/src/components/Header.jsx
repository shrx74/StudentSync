function Header() {
    return (
        <header className="header">
            <div className="logo">Student<span className="logo-sync">Sync</span></div>
            <nav>
                <span className="active">Dashboard</span>
                <span>Academics</span>
                <span>Work</span>
                <span>Budgeting</span>
            </nav>
        </header>
    )
}

export default Header