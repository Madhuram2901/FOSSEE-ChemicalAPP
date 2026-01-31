import { useState } from "react";

export default function UploadForm({ onUpload, loading }) {
    const [dragActive, setDragActive] = useState(false);
    const [fileName, setFileName] = useState("");
    const [localError, setLocalError] = useState(null);

    const handleDrag = (e) => {
        e.preventDefault(); e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") setDragActive(true);
        else if (e.type === "dragleave") setDragActive(false);
    };

    const handleDrop = (e) => {
        e.preventDefault(); e.stopPropagation();
        setDragActive(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFile(e.dataTransfer.files[0]);
        }
    };

    const handleChange = (e) => {
        e.preventDefault();
        if (e.target.files && e.target.files[0]) {
            handleFile(e.target.files[0]);
        }
    };

    const handleFile = (file) => {
        if (loading) {
            // Avoid queuing uploads while a request is already in progress
            return;
        }
        setLocalError(null);
        if (!file.name.endsWith(".csv")) {
            setLocalError("Please upload a valid .csv file.");
            return;
        }
        setFileName(file.name);
        onUpload(file);
    };

    const clearFile = () => {
        setFileName("");
        setLocalError(null);
    };

    return (
        <div className="bg-app-surface p-6 rounded-2xl shadow-xl h-fit">
            <div className="mb-6">
                <h3 className="text-lg font-semibold text-content-main">Upload CSV</h3>
                <p className="text-content-muted text-sm mt-1">
                    Upload your equipment data file
                </p>
            </div>

            <div
                className={`relative border-2 border-dashed rounded-xl p-8 text-center transition-all ${dragActive
                        ? "border-primary bg-primary-light scale-[1.02]"
                        : "border-gray-400 hover:border-primary"
                    } ${loading ? "opacity-50 cursor-not-allowed" : ""}`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
            >
                {!loading && (
                    <input
                        type="file"
                        accept=".csv"
                        onChange={handleChange}
                        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                    />
                )}

                <div className="text-4xl mb-3">
                    {loading ? "⏳" : fileName ? "✅" : "📁"}
                </div>

                {loading ? (
                    <div className="space-y-2">
                        <p className="text-primary font-medium animate-pulse">Processing data...</p>
                        <div className="w-full bg-app-bg h-1 rounded-full overflow-hidden">
                            <div className="bg-primary h-full animate-progress-fast shadow-[0_0_10px_#2196f3]"></div>
                        </div>
                    </div>
                ) : fileName ? (
                    <div className="flex flex-col items-center">
                        <p className="text-content-main font-semibold truncate max-w-full px-4">{fileName}</p>
                        <button
                            onClick={clearFile}
                            className="mt-2 text-xs text-red-500 hover:underline font-medium"
                        >
                            Change file
                        </button>
                    </div>
                ) : (
                    <div>
                        <p className="text-content-main font-medium">Drop your CSV file here</p>
                        <p className="text-content-muted text-sm mt-1">or click to browse</p>
                    </div>
                )}
            </div>

            {localError && (
                <div className="mt-4 p-3 bg-red-50 text-red-600 text-xs rounded-xl border border-red-100 font-medium">
                    ⚠️ {localError}
                </div>
            )}

            <div className="mt-6 p-4 bg-app-bg rounded-xl">
                <p className="text-sm font-medium text-content-main mb-2">Required columns:</p>
                <ul className="grid grid-cols-2 gap-2">
                    {["Name", "Type", "Flowrate", "Pressure", "Temperature"].map(col => (
                        <li key={col} className="text-[10px] text-content-muted flex items-center">
                            <span className="w-1.5 h-1.5 bg-primary rounded-full mr-2"></span>
                            {col}
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
}

