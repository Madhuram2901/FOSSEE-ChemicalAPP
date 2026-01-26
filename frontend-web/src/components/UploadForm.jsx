import { useState } from "react";

export default function UploadForm({ onUpload, loading }) {
    const [dragActive, setDragActive] = useState(false);
    const [fileName, setFileName] = useState("");

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
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
        setFileName(file.name);
        onUpload(file);
    };

    return (
        <div className="bg-app-surface p-6 rounded-2xl shadow-xl h-fit">
            {/* Header */}
            <div className="mb-6">
                <h3 className="text-lg font-semibold text-content-main">Upload CSV</h3>
                <p className="text-content-muted text-sm mt-1">
                    Upload your equipment data file
                </p>
            </div>

            {/* Upload Area */}
            <div
                className={`relative border-2 border-dashed rounded-xl p-8 text-center transition-colors ${dragActive
                    ? "border-primary bg-primary-light"
                    : "border-gray-400 hover:border-primary"
                    }`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
            >
                <input
                    type="file"
                    accept=".csv"
                    onChange={handleChange}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                    disabled={loading}
                />

                <div className="text-4xl mb-3">📁</div>

                {loading ? (
                    <p className="text-primary font-medium">Processing...</p>
                ) : fileName ? (
                    <p className="text-content-main font-medium">{fileName}</p>
                ) : (
                    <>
                        <p className="text-content-main font-medium">
                            Drop your CSV file here
                        </p>
                        <p className="text-content-muted text-sm mt-1">
                            or click to browse
                        </p>
                    </>
                )}
            </div>

            {/* Requirements */}
            <div className="mt-6 p-4 bg-app-bg rounded-xl">
                <p className="text-sm font-medium text-content-main mb-2">Required columns:</p>
                <ul className="text-xs text-content-muted space-y-1">
                    <li>• Equipment Name</li>
                    <li>• Type</li>
                    <li>• Flowrate</li>
                    <li>• Pressure</li>
                    <li>• Temperature</li>
                </ul>
            </div>
        </div>
    );
}
