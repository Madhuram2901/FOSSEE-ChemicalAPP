import "../styles/DataTable.css";

export default function DataTable({ rows }) {
    if (!rows || !rows.length) return null;

    const columns = Object.keys(rows[0]);

    return (
        <div className="table-container">
            <h3 className="table-title">Equipment Data</h3>
            <div className="table-wrapper">
                <table className="data-table">
                    <thead>
                        <tr>
                            {columns.map((col) => (
                                <th key={col}>{col}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {rows.map((row, i) => (
                            <tr key={i}>
                                {columns.map((col) => (
                                    <td key={col}>{row[col]}</td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
