export default function DataTable({ rows }) {
    if (!rows || !rows.length) return null;

    const columns = Object.keys(rows[0]);

    return (
        <div className="bg-app-surface rounded-2xl shadow-sm border border-app-border overflow-hidden">
            <div className="p-6 border-b border-app-border">
                <h3 className="text-lg font-semibold text-content-main">Equipment Data</h3>
                <p className="text-content-muted text-sm mt-1">{rows.length} items</p>
            </div>

            <div className="overflow-x-auto">
                <table className="w-full">
                    <thead>
                        <tr className="bg-app-bg">
                            {columns.map((col) => (
                                <th
                                    key={col}
                                    className="px-6 py-4 text-left text-xs font-semibold text-content-muted uppercase tracking-wider"
                                >
                                    {col}
                                </th>
                            ))}
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-app-border">
                        {rows.map((row, i) => (
                            <tr key={i} className="hover:bg-app-bg transition-colors">
                                {columns.map((col) => (
                                    <td
                                        key={col}
                                        className="px-6 py-4 text-sm text-content-main whitespace-nowrap"
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
