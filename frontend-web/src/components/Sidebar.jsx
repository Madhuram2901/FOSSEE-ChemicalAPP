export default function Sidebar() {
    return (
        <div className="w-20 bg-white shadow-lg flex flex-col items-center py-6 space-y-8">
            {/* Logo */}
            <div className="w-12 h-12 bg-blue-600 rounded-xl flex items-center justify-center">
                <span className="text-white text-xl font-bold">CE</span>
            </div>

            {/* Navigation */}
            <nav className="flex flex-col items-center space-y-6 flex-1">
                <button
                    className="w-12 h-12 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center hover:bg-blue-100 transition-colors"
                    title="Dashboard"
                >
                    <span className="text-xl">📊</span>
                </button>

                <button
                    className="w-12 h-12 rounded-xl text-gray-400 flex items-center justify-center hover:bg-gray-100 transition-colors"
                    title="Upload"
                >
                    <span className="text-xl">📁</span>
                </button>

                <button
                    className="w-12 h-12 rounded-xl text-gray-400 flex items-center justify-center hover:bg-gray-100 transition-colors"
                    title="History"
                >
                    <span className="text-xl">📜</span>
                </button>

                <button
                    className="w-12 h-12 rounded-xl text-gray-400 flex items-center justify-center hover:bg-gray-100 transition-colors"
                    title="About"
                >
                    <span className="text-xl">ℹ️</span>
                </button>
            </nav>

            {/* Settings */}
            <button
                className="w-12 h-12 rounded-xl text-gray-400 flex items-center justify-center hover:bg-gray-100 transition-colors"
                title="Settings"
            >
                <span className="text-xl">⚙️</span>
            </button>
        </div>
    );
}
