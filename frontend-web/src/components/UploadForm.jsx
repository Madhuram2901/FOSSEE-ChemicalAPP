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
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 h-fit">
            {/* Header */}
            <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-900">Upload CSV</h3>
                <p className="text-gray-500 text-sm mt-1">
                    Upload your equipment data file
                </p>
            </div>

            {/* Upload Area */}
            <div
                className={`relative border-2 border-dashed rounded-xl p-8 text-center transition-colors ${dragActive
                        ? "border-blue-500 bg-blue-50"
                        : "border-gray-200 hover:border-gray-300"
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
                    <p className="text-blue-600 font-medium">Processing...</p>
                ) : fileName ? (
                    <p className="text-gray-700 font-medium">{fileName}</p>
                ) : (
                    <>
                        <p className="text-gray-700 font-medium">
                            Drop your CSV file here
                        </p>
                        <p className="text-gray-400 text-sm mt-1">
                            or click to browse
                        </p>
                    </>
                )}
            </div>

            {/* Requirements */}
            <div className="mt-6 p-4 bg-gray-50 rounded-xl">
                <p className="text-sm font-medium text-gray-700 mb-2">Required columns:</p>
                <ul className="text-xs text-gray-500 space-y-1">
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
