import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { motion } from 'framer-motion';
import { ArrowRight, Lock, User, AlertCircle, Beaker } from 'lucide-react';

import { API_BASE_URL } from '../config';

const API = API_BASE_URL;

export default function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');

        try {
            const response = await axios.post(`${API}/token/`, {
                username,
                password,
            });

            const { access, refresh } = response.data;
            localStorage.setItem('auth_token', access);
            localStorage.setItem('refresh_token', refresh);

            // Navigate to dashboard
            navigate('/');
        } catch (err) {
            setError('Invalid credentials. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        /* --- MAIN PAGE BACKGROUND COLOR --- */
        /* Change bg-[#FFEEA9] to your desired color */
        <div className="min-h-screen flex items-center justify-center bg-[#FFEEA9] relative overflow-hidden">


            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="w-full max-w-md z-10 p-4"
            >
                {/* --- LOGIN CARD/BOX BACKGROUND --- */}
                {/* Change bg-white/10 to bg-[#Color] if you want a solid box, or keep it for glass effect */}
                <div className="bg-[#7B4019] backdrop-blur-2xl border border-white/20 rounded-3xl shadow-2xl overflow-hidden">
                    <div className="p-8">
                        <div className="flex justify-center mb-6">
                            <div className="w-16 h-16 bg-[#4F200D] rounded-2xl flex items-center justify-center shadow-lg transform rotate-3">
                                <Beaker className="w-8 h-8 text-white" />
                            </div>
                        </div>

                        <h2 className="text-3xl font-bold text-center text-white mb-2">Welcome Back</h2>
                        <p className="text-center text-white mb-8">Sign in to access your analytics dashboard</p>

                        {error && (
                            <motion.div
                                initial={{ opacity: 0, height: 0 }}
                                animate={{ opacity: 1, height: 'auto' }}
                                className="bg-red-500/10 border border-red-500/20 text-red-200 px-4 py-3 rounded-xl flex items-center gap-3 mb-6 text-sm"
                            >
                                <AlertCircle className="w-4 h-4" />
                                {error}
                            </motion.div>
                        )}

                        <form onSubmit={handleLogin} className="space-y-5">
                            <div className="relative group">
                                <User className="absolute left-4 top-3.5 w-5 h-5 text-black group-focus-within:text-blue-400 transition-colors" />
                                <input
                                    type="text"
                                    placeholder="Username"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                    className="w-full bg-gray-900/50 border border-black text-white rounded-xl py-3 pl-12 pr-4 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all placeholder:text-gray-500"
                                    required
                                />
                            </div>

                            <div className="relative group">
                                <Lock className="absolute left-4 top-3.5 w-5 h-5 text-black group-focus-within:text-blue-400 transition-colors" />
                                <input
                                    type="password"
                                    placeholder="Password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="w-full bg-gray-900/50 border border-black text-white rounded-xl py-3 pl-12 pr-4 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all placeholder:text-gray-500"
                                    required
                                />
                            </div>

                            <div className="flex items-center justify-between text-sm">
                                <label className="flex items-center gap-2 text-[#FFF287] cursor-pointer hover:text-gray-300">
                                    <input type="checkbox" className="w-4 h-4 rounded bg-gray-800 border-gray-700 text-blue-500 focus:ring-blue-500 focus:ring-offset-gray-900" />
                                    Remember me
                                </label>
                                <a href="#" className="text-[#FFF287] hover:text-blue-300 transition-colors">Forgot password?</a>
                            </div>

                            <button
                                type="submit"
                                disabled={isLoading}
                                className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white font-semibold py-3.5 rounded-xl shadow-lg shadow-blue-600/30 flex items-center justify-center gap-2 transition-all transform active:scale-95 disabled:opacity-70 disabled:cursor-not-allowed"
                            >
                                {isLoading ? (
                                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                                ) : (
                                    <>
                                        Sign In
                                        <ArrowRight className="w-5 h-5" />
                                    </>
                                )}
                            </button>
                        </form>
                    </div>

                    <div className="bg-gray-900/50 border-t border-white/5 p-6 text-center">
                        <p className="text-gray-400 text-sm">
                            Don't have an account?{' '}
                            <Link to="/signup" className="text-blue-400 font-semibold hover:text-blue-300 transition-colors">
                                Create Account
                            </Link>
                        </p>
                    </div>
                </div>
            </motion.div>
        </div>
    );
}
