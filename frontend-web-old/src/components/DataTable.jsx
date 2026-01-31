import { useState } from "react";

export default function DataTable({ rows }) {
    const [sortConfig, setSortConfig] = useState({ key: null, direction: "asc" });
    const [searchQuery, setSearchQuery] = useState("");

    if (!rows || !rows.length) return null;

    const columns = Object.keys(rows[0]);

    // Handle sorting
    const requestSort = (key) => {
        let direction = "asc";
        if (sortConfig.key === key && sortConfig.direction === "asc") {
            direction = "desc";
        }
        setSortConfig({ key, direction });
    };

    // Filter and Sort data
    const processedRows = [...rows]
        .filter((row) => {
            if (!searchQuery) return true;
            // Search is focused on the Equipment Name column to make it predictable
            const nameValue =
                row["Equipment Name"] ??
                row["equipment_name"] ??
                row["Name"] ??
                "";
            return String(nameValue)
                .toLowerCase()
                .includes(searchQuery.toLowerCase());
        })
        .sort((a, b) => {
            if (!sortConfig.key) return 0;
            const aVal = a[sortConfig.key];
            const bVal = b[sortConfig.key];

            // Handle null/undefined values by pushing them to the bottom
            if (aVal == null && bVal == null) return 0;
            if (aVal == null) return 1;
            if (bVal == null) return -1;

            const aNum = typeof aVal === "number" ? aVal : parseFloat(aVal);
            const bNum = typeof bVal === "number" ? bVal : parseFloat(bVal);
            const bothNumeric = !Number.isNaN(aNum) && !Number.isNaN(bNum);

            let comparison = 0;
            if (bothNumeric) {
                if (aNum < bNum) comparison = -1;
                else if (aNum > bNum) comparison = 1;
            } else {
                const aStr = String(aVal).toLowerCase();
                const bStr = String(bVal).toLowerCase();
                if (aStr < bStr) comparison = -1;
                else if (aStr > bStr) comparison = 1;
            }

            return sortConfig.direction === "asc" ? comparison : -comparison;
        });

    return (
        <div className="bg-app-surface rounded-2xl shadow-md overflow-hidden">
            <div className="p-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h3 className="text-lg font-semibold text-content-main">Equipment Data</h3>
                    <p className="text-content-muted text-sm mt-1">
                        Displaying {processedRows.length} of {rows.length} items
                    </p>
                </div>

                <div className="relative">
                    <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">🔍</span>
                    <input
                        type="text"
                        placeholder="Search equipment..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="pl-10 pr-4 py-2 bg-app-bg border-none rounded-xl text-sm focus:ring-2 focus:ring-primary w-full md:w-64"
                    />
                </div>
            </div>

            <div className="overflow-x-auto">
                <table className="w-full">
                    <thead>
                        <tr className="bg-app-bg">
                            {columns.map((col) => (
                                <th
                                    key={col}
                                    onClick={() => requestSort(col)}
                                    className="px-6 py-4 text-left text-xs font-semibold text-content-muted uppercase tracking-wider cursor-pointer hover:text-primary transition-colors"
                                >
                                    <div className="flex items-center">
                                        {col}
                                        {sortConfig.key === col && (
                                            <span className="ml-1">{sortConfig.direction === "asc" ? "🔼" : "🔽"}</span>
                                        )}
                                    </div>
                                </th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {processedRows.map((row, i) => (
                            <tr key={i} className="hover:bg-app-bg transition-colors border-b border-gray-100 last:border-0">
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
                {processedRows.length === 0 && (
                    <div className="p-12 text-center text-content-muted">
                        No matching equipment found.
                    </div>
                )}
            </div>
        </div>
    );
}

