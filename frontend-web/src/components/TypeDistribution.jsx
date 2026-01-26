export default function TypeDistribution({ distribution }) {
    if (!distribution) return null;

    const total = Object.values(distribution).reduce((a, b) => a + b, 0);
    const colors = [
        "bg-blue-500",
        "bg-green-500",
        "bg-yellow-500",
        "bg-red-500",
        "bg-purple-500",
        "bg-pink-500",
        "bg-cyan-500",
        "bg-lime-500",
    ];

    return (
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Equipment Types</h3>

            <div className="space-y-4">
                {Object.entries(distribution).map(([type, count], index) => {
                    const percentage = Math.round((count / total) * 100);
                    return (
                        <div key={type}>
                            <div className="flex justify-between items-center mb-2">
                                <span className="text-sm font-medium text-gray-700">{type}</span>
                                <span className="text-sm text-gray-500">{count} ({percentage}%)</span>
                            </div>
                            <div className="w-full h-2 bg-gray-100 rounded-full overflow-hidden">
                                <div
                                    className={`h-full ${colors[index % colors.length]} rounded-full transition-all duration-500`}
                                    style={{ width: `${percentage}%` }}
                                />
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
