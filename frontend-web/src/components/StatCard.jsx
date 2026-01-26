export default function StatCard({ title, value, subtitle, icon }) {
    return (
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <div className="flex items-center justify-between">
                <div>
                    <p className="text-gray-500 text-sm font-medium">{title}</p>
                    <p className="text-3xl font-bold text-gray-900 mt-2">{value}</p>
                    {subtitle && (
                        <p className="text-green-600 text-sm mt-1 font-medium">{subtitle}</p>
                    )}
                </div>
                {icon && (
                    <div className="w-14 h-14 bg-blue-50 rounded-2xl flex items-center justify-center">
                        <span className="text-2xl">{icon}</span>
                    </div>
                )}
            </div>
        </div>
    );
}
