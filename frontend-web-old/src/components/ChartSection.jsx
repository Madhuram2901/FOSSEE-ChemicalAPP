import { useState } from "react";
import { Bar, Pie, Line } from "react-chartjs-2";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    PointElement,
    LineElement,
    ArcElement,
    Tooltip,
    Legend,
} from "chart.js";

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    PointElement,
    LineElement,
    ArcElement,
    Tooltip,
    Legend
);

const barColors = ["#10b981", "#f59e0b", "#ef4444"];
const pieColors = [
    "#2563eb",
    "#10b981",
    "#f59e0b",
    "#ef4444",
    "#8b5cf6",
    "#ec4899",
    "#06b6d4",
    "#84cc16",
];

export default function ChartSection({ data }) {
    const [chartType, setChartType] = useState("bar"); // 'bar' or 'line'

    if (!data) return null;

    const avgData = {
        labels: ["Flowrate (m³/h)", "Pressure (bar)", "Temperature (°C)"],
        datasets: [
            {
                label: "Average Values",
                data: [data.averages.flowrate, data.averages.pressure, data.averages.temperature],
                backgroundColor: chartType === "bar" ? barColors : "rgba(37, 99, 235, 0.1)",
                borderColor: chartType === "line" ? "#2563eb" : "transparent",
                borderWidth: 2,
                borderRadius: 8,
                barThickness: 40,
                tension: 0.4,
                fill: true,
            },
        ],
    };

    const avgOptions = {
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
                grid: { color: "#f1f5f9" },
                ticks: { color: "#64748b" },
            },
            x: {
                grid: { display: false },
                ticks: { color: "#64748b" },
            },
        },
    };

    const pieData = {
        labels: Object.keys(data.type_distribution),
        datasets: [
            {
                data: Object.values(data.type_distribution),
                backgroundColor: pieColors.slice(0, Object.keys(data.type_distribution).length),
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
                    color: "#0f172a",
                    padding: 16,
                    usePointStyle: true,
                    font: { size: 12 },
                },
            },
        },
    };

    return (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Average Parameters Chart */}
            <div className="bg-app-surface p-6 rounded-2xl shadow-md">
                <div className="flex justify-between items-center mb-4">
                    <h3 className="text-lg font-semibold text-content-main">Average Parameters</h3>
                    <div className="flex bg-app-bg p-1 rounded-lg">
                        <button
                            onClick={() => setChartType("bar")}
                            className={`px-3 py-1 text-xs rounded-md transition-all ${chartType === "bar" ? "bg-primary text-white shadow-sm" : "text-content-muted"
                                }`}
                        >
                            Bar
                        </button>
                        <button
                            onClick={() => setChartType("line")}
                            className={`px-3 py-1 text-xs rounded-md transition-all ${chartType === "line" ? "bg-primary text-white shadow-sm" : "text-content-muted"
                                }`}
                        >
                            Line
                        </button>
                    </div>
                </div>
                <div className="h-64">
                    {chartType === "bar" ? (
                        <Bar data={avgData} options={avgOptions} />
                    ) : (
                        <Line data={avgData} options={avgOptions} />
                    )}
                </div>
            </div>

            {/* Pie Chart */}
            <div className="bg-app-surface p-6 rounded-2xl shadow-md">
                <h3 className="text-lg font-semibold text-content-main mb-4">
                    Equipment Type Distribution
                </h3>
                <div className="h-64">
                    <Pie data={pieData} options={pieOptions} />
                </div>
            </div>
        </div>
    );
}

