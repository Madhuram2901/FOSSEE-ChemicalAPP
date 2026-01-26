import { useState } from "react";
import axios from "axios";
import SummaryCards from "../components/SummaryCards";
import Charts from "../components/Charts";
import DataTable from "../components/DataTable";
import "../styles/Dashboard.css";

const API = "http://localhost:8000/api";

export default function Dashboard() {
    const [summary, setSummary] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const uploadFile = async (e) => {
        const file = e.target.files[0];
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
        <div className="dashboard">
            <header className="dashboard-header">
                <h1 className="dashboard-title">Chemical Equipment Parameter Visualizer</h1>
                <p className="dashboard-subtitle">Upload CSV data to analyze equipment parameters</p>
            </header>

            <div className="upload-section">
                <label className="upload-label" htmlFor="csv-upload">
                    <span className="upload-icon">📁</span>
                    <span className="upload-text">
                        {loading ? "Processing..." : "Click to upload CSV file"}
                    </span>
                    <input
                        type="file"
                        id="csv-upload"
                        accept=".csv"
                        onChange={uploadFile}
                        disabled={loading}
                        className="upload-input"
                    />
                </label>
            </div>

            {error && (
                <div className="error-message">
                    <span>⚠️ {error}</span>
                </div>
            )}

            {summary && (
                <div className="dashboard-content">
                    <SummaryCards data={summary} />
                    <Charts data={summary} />
                    <DataTable rows={summary.table} />
                </div>
            )}
        </div>
    );
}
