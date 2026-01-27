import { useState, useEffect } from "react";
import axios from "axios";
import Sidebar from "../components/Sidebar";
import StatCard from "../components/StatCard";
import ChartSection from "../components/ChartSection";
import UploadForm from "../components/UploadForm";
import DataTable from "../components/DataTable";
import TypeDistribution from "../components/TypeDistribution";
import HistoryList from "../components/HistoryList";
import flowrateIcon from "../assets/flowrate.png";
import chemistryIcon from "../assets/chemistry.png";
import pressureIcon from "../assets/pressure.png";
import temperatureIcon from "../assets/temperature.png";

// Icon Attributions:
// Flow rate: https://www.flaticon.com/free-icons/flow-rate
// Chemistry: https://www.flaticon.com/free-icons/chemistry
// Pressure: https://www.flaticon.com/free-icons/pressure
// Temperature: Provided by user (via Flaticon)

const API = "http://localhost:8000/api";

export default function Dashboard() {
    const [summary, setSummary] = useState(null);
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(false);
    const [fetchingHistory, setFetchingHistory] = useState(false);
    const [selectedDatasetId, setSelectedDatasetId] = useState(null);
    const [showAveragesChart, setShowAveragesChart] = useState(true);
    const [showTypeDistributionChart, setShowTypeDistributionChart] = useState(true);
    const [error, setError] = useState(null);
    const [successMessage, setSuccessMessage] = useState(null);

    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        setFetchingHistory(true);
        try {
            const res = await axios.get(`${API}/history/`);
            setHistory(res.data);
            // If we have history and no current summary, load the latest one
            if (res.data.length > 0 && !summary) {
                const latestId = res.data[0].id;
                setSelectedDatasetId(latestId);
                handleSelectDataset(latestId);
            }
        } catch (err) {
            console.error("Failed to fetch history");
            setError("Failed to fetch dataset history. Please try again.");
        } finally {
            setFetchingHistory(false);
        }
    };

    const handleSelectDataset = async (id) => {
        if (!id) return;
        setSelectedDatasetId(id);
        setLoading(true);
        setError(null);
        setSuccessMessage(null);
        try {
            const res = await axios.get(`${API}/summary/${id}/`);
            setSummary(res.data);
        } catch (err) {
            setError("Failed to load dataset details");
        } finally {
            setLoading(false);
        }
    };

    const handleUpload = async (file) => {
        if (!file) return;

        setLoading(true);
        setError(null);
        setSuccessMessage(null);

        const formData = new FormData();
        formData.append("file", file);

        try {
            const res = await axios.post(`${API}/upload/`, formData);
            setSuccessMessage("File uploaded and processed successfully!");
            await fetchHistory(); // Refresh history
            await handleSelectDataset(res.data.dataset_id); // Load the new dataset
        } catch (err) {
            setError(err.response?.data?.error || "Failed to upload file");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex h-screen bg-app-bg">
            {/* Sidebar */}
            <Sidebar />

            {/* Main Content */}
            <div className="flex-1 overflow-auto">
                {/* Header */}
                <header className="bg-app-surface shadow-md px-8 py-6 z-10">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-2xl font-bold text-content-main">
                                Chemical Equipment Visualizer
                            </h1>
                            <p className="text-content-muted mt-1">CSV Analytics Dashboard</p>
                        </div>
                        <div className="flex items-center space-x-4">
                            {loading && (
                                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-primary mr-4"></div>
                            )}
                            <span className="text-sm text-content-muted">
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
                        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 shadow-md flex items-center justify-between gap-4">
                            <div>
                                <span className="font-medium">Error:</span> {error}
                            </div>
                            <div className="flex items-center gap-2">
                                <button
                                    type="button"
                                    onClick={() => {
                                        // Retry history if we have no datasets yet, otherwise retry the last selected dataset
                                        if (!selectedDatasetId) {
                                            fetchHistory();
                                        } else {
                                            handleSelectDataset(selectedDatasetId);
                                        }
                                    }}
                                    className="px-3 py-1 text-xs font-semibold bg-red-100 text-red-700 rounded-lg hover:bg-red-200 transition-colors"
                                >
                                    Retry
                                </button>
                            </div>
                        </div>
                    )}
                    {successMessage && (
                        <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-xl text-green-700 shadow-md">
                            <span className="font-medium">Success:</span> {successMessage}
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
                                    icon={<img src={chemistryIcon} alt="Chemistry" className="w-12 h-12 object-contain" />}
                                />
                                <StatCard
                                    title="Avg Flowrate"
                                    value={summary ? `${summary.averages.flowrate} m³/h` : "—"}
                                    icon={<img src={flowrateIcon} alt="Flowrate" className="w-9 h-9 object-contain" />}
                                />
                                <StatCard
                                    title="Avg Pressure"
                                    value={summary ? `${summary.averages.pressure} bar` : "—"}
                                    icon={<img src={pressureIcon} alt="Pressure" className="w-12 h-12 object-contain" />}
                                />
                                <StatCard
                                    title="Avg Temperature"
                                    value={summary ? `${summary.averages.temperature} °C` : "—"}
                                    icon={<img src={temperatureIcon} alt="Temperature" className="w-9 h-9 object-contain" />}
                                />
                            </div>

                            {/* Chart visibility controls */}
                            <div className="flex flex-wrap items-center justify-between gap-3">
                                <div className="text-sm text-content-muted">
                                    Toggle analytics views to focus on what matters for this dataset.
                                </div>
                                <div className="flex flex-wrap gap-2">
                                    <button
                                        type="button"
                                        onClick={() => setShowAveragesChart((prev) => !prev)}
                                        className={`px-3 py-1 text-xs rounded-lg border text-content-main transition-colors ${showAveragesChart ? "bg-app-bg border-primary" : "bg-app-bg border-gray-300"
                                            }`}
                                    >
                                        {showAveragesChart ? "Hide" : "Show"} Averages Chart
                                    </button>
                                    <button
                                        type="button"
                                        onClick={() => setShowTypeDistributionChart((prev) => !prev)}
                                        className={`px-3 py-1 text-xs rounded-lg border text-content-main transition-colors ${showTypeDistributionChart ? "bg-app-bg border-primary" : "bg-app-bg border-gray-300"
                                            }`}
                                    >
                                        {showTypeDistributionChart ? "Hide" : "Show"} Type Distribution
                                    </button>
                                </div>
                            </div>

                            {/* Charts */}
                            {summary && showAveragesChart && <ChartSection data={summary} />}

                            {/* Type Distribution */}
                            {summary && showTypeDistributionChart && (
                                <TypeDistribution distribution={summary.type_distribution} />
                            )}

                            {/* Data Table */}
                            {summary && <DataTable rows={summary.table} />}

                            {/* Empty State */}
                            {!summary && !loading && (
                                <div className="bg-app-surface rounded-2xl shadow-xl p-12 text-center">
                                    <div className="text-6xl mb-4">📈</div>
                                    <h3 className="text-xl font-semibold text-content-main mb-2">
                                        No Data Yet
                                    </h3>
                                    <p className="text-content-muted max-w-md mx-auto">
                                        Upload a CSV file containing equipment data to see analytics,
                                        charts, and detailed breakdowns.
                                    </p>
                                </div>
                            )}
                        </div>

                        {/* Right Sidebar - Upload Form & History */}
                        <div className="lg:col-span-1">
                            <UploadForm onUpload={handleUpload} loading={loading} />
                            <HistoryList
                                history={history}
                                onSelect={handleSelectDataset}
                                currentId={summary?.id}
                                loading={loading}
                                fetching={fetchingHistory}
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
