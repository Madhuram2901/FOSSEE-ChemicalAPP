import { Bar, Pie } from "react-chartjs-2";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    ArcElement,
    Tooltip,
    Legend,
} from "chart.js";
import "../styles/Charts.css";

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    ArcElement,
    Tooltip,
    Legend
);

const barColors = ["#3b82f6", "#10b981", "#ef4444"];
const pieColors = [
    "#3b82f6",
    "#10b981",
    "#f59e0b",
    "#ef4444",
    "#8b5cf6",
    "#ec4899",
    "#06b6d4",
    "#84cc16",
];

export default function Charts({ data }) {
    const barData = {
        labels: ["Flowrate (m³/h)", "Pressure (bar)", "Temperature (°C)"],
        datasets: [
            {
                label: "Average Values",
                data: Object.values(data.averages),
                backgroundColor: barColors,
                borderRadius: 8,
            },
        ],
    };

    const barOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false,
            },
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: "rgba(255, 255, 255, 0.1)",
                },
                ticks: {
                    color: "#94a3b8",
                },
            },
            x: {
                grid: {
                    display: false,
                },
                ticks: {
                    color: "#94a3b8",
                },
            },
        },
    };

    const pieData = {
        labels: Object.keys(data.type_distribution),
        datasets: [
            {
                data: Object.values(data.type_distribution),
                backgroundColor: pieColors.slice(
                    0,
                    Object.keys(data.type_distribution).length
                ),
                borderWidth: 0,
            },
        ],
    };

    const pieOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: "right",
                labels: {
                    color: "#e2e8f0",
                    padding: 20,
                    usePointStyle: true,
                },
            },
        },
    };

    return (
        <div className="charts-container">
            <div className="chart-card">
                <h3 className="chart-title">Average Parameters</h3>
                <div className="chart-wrapper">
                    <Bar data={barData} options={barOptions} />
                </div>
            </div>

            <div className="chart-card">
                <h3 className="chart-title">Equipment Type Distribution</h3>
                <div className="chart-wrapper">
                    <Pie data={pieData} options={pieOptions} />
                </div>
            </div>
        </div>
    );
}
