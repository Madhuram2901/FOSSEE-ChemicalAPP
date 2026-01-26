import "../styles/SummaryCards.css";

export default function SummaryCards({ data }) {
    const cards = [
        {
            label: "Total Equipment",
            value: data.total_equipment,
            icon: "🏭",
            color: "#3b82f6",
        },
        {
            label: "Avg Flowrate",
            value: `${data.averages.flowrate} m³/h`,
            icon: "💧",
            color: "#10b981",
        },
        {
            label: "Avg Pressure",
            value: `${data.averages.pressure} bar`,
            icon: "📊",
            color: "#f59e0b",
        },
        {
            label: "Avg Temperature",
            value: `${data.averages.temperature} °C`,
            icon: "🌡️",
            color: "#ef4444",
        },
    ];

    return (
        <div className="summary-cards">
            {cards.map((card, index) => (
                <div
                    key={index}
                    className="summary-card"
                    style={{ borderTopColor: card.color }}
                >
                    <div className="card-icon">{card.icon}</div>
                    <div className="card-content">
                        <span className="card-value">{card.value}</span>
                        <span className="card-label">{card.label}</span>
                    </div>
                </div>
            ))}
        </div>
    );
}
