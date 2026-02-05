'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function Signup() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Basic client-side validation
    if (password.length < 8) {
      setError('Password must be at least 8 characters long');
      return;
    }

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_API_URL}/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        // Auto-login after successful signup
        const loginResponse = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_API_URL}/login`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email, password }),
        });

        const loginData = await loginResponse.json();

        if (loginResponse.ok) {
          // Store the token in localStorage
          localStorage.setItem('token', loginData.access_token);
          // Redirect to dashboard
          router.push('/dashboard');
          router.refresh();
        } else {
          setError(loginData.detail || 'Login failed after signup');
        }
      } else {
        setError(data.detail || 'Signup failed');
      }
    } catch (err) {
      setError('An error occurred. Please try again.');
      console.error(err);
    }
  };

  return (
    <div className="min-h-screen bg-[#050505] flex items-center justify-center p-4 relative overflow-hidden">
      {/* Premium Neon UI - Gradient Background Effects */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-gradient-radial from-purple-500/10 to-transparent rounded-full blur-3xl animate-pulse-slow"></div>
        <div className="absolute bottom-1/3 right-1/4 w-80 h-80 bg-gradient-radial from-blue-500/10 to-transparent rounded-full blur-3xl animate-pulse-slower"></div>
      </div>

      <div className="max-w-md w-full space-y-8 bg-white/5 backdrop-blur-xl p-8 rounded-2xl border border-white/20 z-10 shadow-2xl shadow-purple-500/10">
        <div className="text-center">
          <h2 className="text-4xl font-bold bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent mb-2">Create Account</h2>
          <p className="text-gray-400">Join our premium platform today</p>
        </div>

        {error && (
          <div className="rounded-lg bg-red-900/30 p-4 border border-red-700/50 backdrop-blur-sm">
            <div className="text-sm text-red-300">{error}</div>
          </div>
        )}

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="space-y-4">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-300 mb-2">
                Full Name
              </label>
              <input
                id="name"
                name="name"
                type="text"
                autoComplete="name"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="relative block w-full px-4 py-4 border border-gray-700 placeholder-gray-500 text-white bg-gray-900/50 backdrop-blur-md rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 focus:shadow-[0_0_20px_rgba(168,85,247,0.3)] focus:z-10 transition-all duration-300 hover:border-purple-400/50"
                placeholder="Enter your full name"
              />
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-2">
                Email Address
              </label>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="relative block w-full px-4 py-4 border border-gray-700 placeholder-gray-500 text-white bg-gray-900/50 backdrop-blur-md rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 focus:shadow-[0_0_20px_rgba(168,85,247,0.3)] focus:z-10 transition-all duration-300 hover:border-purple-400/50"
                placeholder="Enter your email"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-300 mb-2">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="new-password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="relative block w-full px-4 py-4 border border-gray-700 placeholder-gray-500 text-white bg-gray-900/50 backdrop-blur-md rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 focus:shadow-[0_0_20px_rgba(168,85,247,0.3)] focus:z-10 transition-all duration-300 hover:border-purple-400/50"
                placeholder="Enter your password (min 8 chars)"
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              className="group relative w-full flex justify-center py-4 px-4 border border-transparent text-lg font-semibold rounded-xl text-white bg-gradient-to-r from-purple-600 via-pink-500 to-blue-500 hover:from-purple-700 hover:via-pink-600 hover:to-blue-600 focus:outline-none focus:ring-2 focus:ring-purple-500/50 transition-all duration-300 hover:scale-[1.02] transform hover:shadow-lg hover:shadow-purple-500/25"
            >
              Create Account
            </button>
          </div>
        </form>

        <div className="text-center text-sm text-gray-400 pt-4">
          Already have an account?{' '}
          <Link href="/login" className="font-medium text-purple-400 hover:text-purple-300 underline transition-colors duration-200">
            Sign in to your account
          </Link>
        </div>
      </div>
    </div>
  );
}