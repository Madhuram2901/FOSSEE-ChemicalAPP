import { useState } from "react";
import axios from "axios";
import Sidebar from "../components/Sidebar";
import StatCard from "../components/StatCard";
import ChartSection from "../components/ChartSection";
import UploadForm from "../components/UploadForm";
import DataTable from "../components/DataTable";
import TypeDistribution from "../components/TypeDistribution";

const API = "http://localhost:8000/api";

export default function Dashboard() {
    const [summary, setSummary] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleUpload = async (file) => {
        if (!file) return;

        setLoading(true);
        setError(null);

        const formData = new FormData();
        formData.append("file", file);

        try {
            const res = await axios.post(`${API}/upload/`, formData);
            const summaryRes = await axios.get(
                `${API}/summary/${res.data.dataset_id}/`
            );
            setSummary(summaryRes.data);
        } catch (err) {
            setError(err.response?.data?.error || "Failed to upload file");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex h-screen bg-gray-50">
            {/* Sidebar */}
            <Sidebar />

            {/* Main Content */}
            <div className="flex-1 overflow-auto">
                {/* Header */}
                <header className="bg-white border-b border-gray-100 px-8 py-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-2xl font-bold text-gray-900">
                                Chemical Equipment Visualizer
                            </h1>
                            <p className="text-gray-500 mt-1">CSV Analytics Dashboard</p>
                        </div>
                        <div className="flex items-center space-x-4">
                            <span className="text-sm text-gray-500">
                                {new Date().toLocaleDateString('en-US', {
                                    weekday: 'long',
                                    year: 'numeric',
                                    month: 'long',
                                    day: 'numeric'
                                })}
                            </span>
                        </div>
                    </div>
                </header>

                {/* Content Area */}
                <div className="p-8">
                    {error && (
                        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700">
                            <span className="font-medium">Error:</span> {error}
                        </div>
                    )}

                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                        {/* Left & Center Content */}
                        <div className="lg:col-span-2 space-y-6">
                            {/* Stats Row */}
                            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
                                <StatCard
                                    title="Total Equipment"
                                    value={summary ? `${summary.total_equipment} units` : "—"}
                                    subtitle={summary ? "Latest upload" : null}
                                    icon="🏭"
                                />
                                <StatCard
                                    title="Avg Flowrate"
                                    value={summary ? `${summary.averages.flowrate} m³/h` : "—"}
                                    icon="💧"
                                />
                                <StatCard
                                    title="Avg Pressure"
                                    value={summary ? `${summary.averages.pressure} bar` : "—"}
                                    icon="📊"
                                />
                                <StatCard
                                    title="Avg Temperature"
                                    value={summary ? `${summary.averages.temperature} °C` : "—"}
                                    icon="🌡️"
                                />
                            </div>

                            {/* Charts */}
                            {summary && <ChartSection data={summary} />}

                            {/* Type Distribution */}
                            {summary && (
                                <TypeDistribution distribution={summary.type_distribution} />
                            )}

                            {/* Data Table */}
                            {summary && <DataTable rows={summary.table} />}

                            {/* Empty State */}
                            {!summary && !loading && (
                                <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-12 text-center">
                                    <div className="text-6xl mb-4">📈</div>
                                    <h3 className="text-xl font-semibold text-gray-900 mb-2">
                                        No Data Yet
                                    </h3>
                                    <p className="text-gray-500 max-w-md mx-auto">
                                        Upload a CSV file containing equipment data to see analytics,
                                        charts, and detailed breakdowns.
                                    </p>
                                </div>
                            )}
                        </div>

                        {/* Right Sidebar - Upload Form */}
                        <div className="lg:col-span-1">
                            <UploadForm onUpload={handleUpload} loading={loading} />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
