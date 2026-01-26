export default function DataTable({ rows }) {
    if (!rows || !rows.length) return null;

    const columns = Object.keys(rows[0]);

    return (
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
            <div className="p-6 border-b border-gray-100">
                <h3 className="text-lg font-semibold text-gray-900">Equipment Data</h3>
                <p className="text-gray-500 text-sm mt-1">{rows.length} items</p>
            </div>

            <div className="overflow-x-auto">
                <table className="w-full">
                    <thead>
                        <tr className="bg-gray-50">
                            {columns.map((col) => (
                                <th
                                    key={col}
                                    className="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider"
                                >
                                    {col}
                                </th>
                            ))}
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                        {rows.map((row, i) => (
                            <tr key={i} className="hover:bg-gray-50 transition-colors">
                                {columns.map((col) => (
                                    <td
                                        key={col}
                                        className="px-6 py-4 text-sm text-gray-700 whitespace-nowrap"
                                    >
                                        {row[col]}
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
