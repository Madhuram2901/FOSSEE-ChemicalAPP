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

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    ArcElement,
    Tooltip,
    Legend
);

export default function ChartSection({ data }) {
    if (!data) return null;

    const barData = {
        labels: ["Flowrate (m³/h)", "Pressure (bar)", "Temperature (°C)"],
        datasets: [
            {
                label: "Average Values",
                data: [data.averages.flowrate, data.averages.pressure, data.averages.temperature],
                backgroundColor: ["#3b82f6", "#10b981", "#f59e0b"],
                borderRadius: 8,
                barThickness: 40,
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
                    color: "#f3f4f6",
                },
                ticks: {
                    color: "#6b7280",
                },
            },
            x: {
                grid: {
                    display: false,
                },
                ticks: {
                    color: "#6b7280",
                },
            },
        },
    };

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
                    color: "#374151",
                    padding: 16,
                    usePointStyle: true,
                    font: {
                        size: 12,
                    },
                },
            },
        },
    };

    return (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Bar Chart */}
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Average Parameters</h3>
                <div className="h-64">
                    <Bar data={barData} options={barOptions} />
                </div>
            </div>

            {/* Pie Chart */}
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Equipment Type Distribution</h3>
                <div className="h-64">
                    <Pie data={pieData} options={pieOptions} />
                </div>
            </div>
        </div>
    );
}
