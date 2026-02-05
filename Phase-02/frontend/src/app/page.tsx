'use client';

import Link from 'next/link';
import { useEffect } from 'react';

export default function Home() {
  // Check if user is logged in and redirect accordingly
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      window.location.href = '/dashboard';
    }
  }, []);

  return (
    <div className="min-h-screen bg-[#050505] flex items-center justify-center p-4 relative overflow-hidden">
      {/* Premium Neon UI - Gradient Background Effects */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
        <div className="absolute top-1/3 left-1/5 w-80 h-80 bg-gradient-radial from-blue-500/10 to-transparent rounded-full blur-3xl animate-pulse-slower"></div>
        <div className="absolute bottom-1/4 right-1/3 w-96 h-96 bg-gradient-radial from-purple-500/10 to-transparent rounded-full blur-3xl animate-pulse-slow"></div>
      </div>

      <div className="max-w-md w-full space-y-8 bg-white/5 backdrop-blur-xl p-8 rounded-2xl border border-white/20 z-10 shadow-2xl shadow-blue-500/10">
        <div className="text-center">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent mb-2">Todo App</h1>
          <p className="text-gray-400">Manage your tasks efficiently</p>
        </div>

        <div className="mt-8 space-y-4">
          <Link href="/login" className="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-gradient-to-r from-blue-600 via-purple-500 to-pink-500 hover:from-blue-700 hover:via-purple-600 hover:to-pink-600 focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all duration-300 hover:scale-[1.02] transform hover:shadow-lg hover:shadow-blue-500/25">
            Sign In
          </Link>

          <Link href="/signup" className="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-gradient-to-r from-purple-600 via-pink-500 to-blue-500 hover:from-purple-700 hover:via-pink-600 hover:to-blue-600 focus:outline-none focus:ring-2 focus:ring-purple-500/50 transition-all duration-300 hover:scale-[1.02] transform hover:shadow-lg hover:shadow-purple-500/25">
            Sign Up
          </Link>
        </div>
      </div>
    </div>
  );
}