function StatCard({ title, value }) {
    return (
        <article className="stat-card">
            <h3>{title}</h3>
            <strong>{value}</strong>
        </article>
    )
}

export default StatCard