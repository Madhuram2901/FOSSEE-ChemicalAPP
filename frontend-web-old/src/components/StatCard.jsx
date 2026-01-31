export default function StatCard({ title, value, subtitle, icon }) {
    return (
        <div className="bg-app-surface p-6 rounded-2xl shadow-xl">
            <div className="flex items-center justify-between">
                <div>
                    <p className="text-content-muted text-sm font-medium">{title}</p>
                    <p className="text-3xl font-bold text-content-main mt-2">{value}</p>
                    {subtitle && (
                        <p className="text-flowrate text-sm mt-1 font-medium">{subtitle}</p>
                    )}
                </div>
                {icon && (
                    <div className="w-14 h-14 bg-primary-light rounded-2xl flex items-center justify-center">
                        <span className="text-2xl">{icon}</span>
                    </div>
                )}
            </div>
        </div>
    );
}
