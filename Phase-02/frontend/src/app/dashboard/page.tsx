'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';

// Define types
type Todo = {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  priority: string;
  user_id: number;
  created_at: string;
  updated_at: string;
};

export default function Dashboard() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [newTodo, setNewTodo] = useState({ title: '', description: '', priority: 'medium' });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const router = useRouter();

  // Check authentication on component mount
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
      return;
    }

    fetchTodos();
  }, [router]);

  const fetchTodos = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_API_URL}/todos`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.status === 401) {
        // Unauthorized - redirect to login
        localStorage.removeItem('token');
        router.push('/login');
        return;
      }

      if (response.ok) {
        const data = await response.json();
        setTodos(data);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to fetch todos');
      }
    } catch (err) {
      setError('An error occurred while fetching todos');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddTodo = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!newTodo.title.trim()) {
      setError('Title is required');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_API_URL}/todos`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          title: newTodo.title,
          description: newTodo.description,
          priority: newTodo.priority,
        }),
      });

      if (response.ok) {
        const createdTodo = await response.json();
        setTodos([...todos, createdTodo]);
        setNewTodo({ title: '', description: '', priority: 'medium' });
        setError('');
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to add todo');
      }
    } catch (err) {
      setError('An error occurred while adding todo');
      console.error(err);
    }
  };

  const toggleTodo = async (id: number, completed: boolean) => {
    try {
      const token = localStorage.getItem('token');
      const todo = todos.find(t => t.id === id);

      if (!todo) {
        setError('Todo not found');
        return;
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_API_URL}/todos/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          completed: !completed,
          priority: todo.priority,
          title: todo.title,
          description: todo.description
        }),
      });

      if (response.ok) {
        const updatedTodo = await response.json();
        setTodos(todos.map(todoItem =>
          todoItem.id === id ? updatedTodo : todoItem
        ));
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to update todo');
      }
    } catch (err) {
      setError('An error occurred while updating todo');
      console.error(err);
    }
  };

  const deleteTodo = async (id: number) => {
    if (!window.confirm('Are you sure you want to delete this todo?')) {
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_API_URL}/todos/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        setTodos(prevTodos => prevTodos.filter(todo => todo.id !== id));
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to delete todo');
      }
    } catch (err) {
      setError('An error occurred while deleting todo');
      console.error(err);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    router.push('/login');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0a0a0a] text-white flex items-center justify-center relative overflow-hidden">
        {/* Premium Neon UI - Gradient Background Effects */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-1/3 left-1/5 w-80 h-80 bg-gradient-radial from-blue-500/20 via-purple-500/20 to-transparent rounded-full blur-3xl animate-pulse-slower"></div>
          <div className="absolute bottom-1/4 right-1/3 w-96 h-96 bg-gradient-radial from-purple-500/20 via-pink-500/20 to-transparent rounded-full blur-3xl animate-pulse-slow"></div>
        </div>

        <div className="text-center relative z-10">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-cyan-400 mx-auto shadow-lg shadow-cyan-400/50"></div>
          <p className="mt-4 text-gray-400 font-mono">Loading your todos...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white relative overflow-hidden">
      {/* Premium Neon UI - Gradient Background Effects */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-gradient-radial from-blue-500/15 via-purple-500/15 to-transparent rounded-full blur-3xl animate-pulse-slow"></div>
        <div className="absolute bottom-1/3 right-1/4 w-80 h-80 bg-gradient-radial from-purple-500/15 via-pink-500/15 to-transparent rounded-full blur-3xl animate-pulse-slower"></div>
      </div>

      <nav className="relative z-10 bg-[#0a0a0a]/80 backdrop-blur-xl border-b border-cyan-500/30 shadow-lg shadow-cyan-500/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold font-mono bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">Todo Dashboard</h1>
            </div>
            <div className="flex items-center">
              <button
                onClick={handleLogout}
                className="ml-4 px-4 py-2 text-sm font-medium text-white bg-gradient-to-r from-red-600 to-red-700 rounded-xl hover:from-red-700 hover:to-red-800 focus:outline-none focus:ring-2 focus:ring-red-500/50 transition-all duration-300 hover:scale-105 transform hover:shadow-lg hover:shadow-red-500/30 border border-red-500/50"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="relative z-10 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-6 rounded-xl bg-red-900/30 p-4 border border-red-700/50 backdrop-blur-sm shadow-lg shadow-red-500/20"
          >
            <div className="text-sm text-red-300 font-mono">{error}</div>
          </motion.div>
        )}

        {/* Add Todo Form - Glassmorphism Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white/5 backdrop-blur-xl rounded-2xl p-8 mb-8 border border-cyan-500/30 shadow-2xl shadow-cyan-500/20"
        >
          <h2 className="text-xl font-semibold font-mono bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent mb-6">Add New Todo</h2>
          <form onSubmit={handleAddTodo} className="space-y-6">
            <div>
              <label htmlFor="title" className="block text-sm font-medium text-cyan-300 mb-2 font-mono">
                Title *
              </label>
              <input
                type="text"
                id="title"
                value={newTodo.title}
                onChange={(e) => setNewTodo({...newTodo, title: e.target.value})}
                className="relative block w-full px-4 py-3 border border-cyan-500/50 placeholder-cyan-500/50 text-white bg-black/30 backdrop-blur-md rounded-xl focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-500/50 focus:shadow-[0_0_20px_rgba(6,182,212,0.4)] focus:z-10 transition-all duration-300 hover:border-cyan-400/70 font-mono"
                placeholder="What needs to be done?"
                required
              />
            </div>
            <div>
              <label htmlFor="description" className="block text-sm font-medium text-cyan-300 mb-2 font-mono">
                Description
              </label>
              <textarea
                id="description"
                value={newTodo.description}
                onChange={(e) => setNewTodo({...newTodo, description: e.target.value})}
                rows={3}
                className="relative block w-full px-4 py-3 border border-cyan-500/50 placeholder-cyan-500/50 text-white bg-black/30 backdrop-blur-md rounded-xl focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-500/50 focus:shadow-[0_0_20px_rgba(6,182,212,0.4)] focus:z-10 transition-all duration-300 hover:border-cyan-400/70 font-mono"
                placeholder="Additional details..."
              ></textarea>
            </div>
            <div>
              <label htmlFor="priority" className="block text-sm font-medium text-cyan-300 mb-2 font-mono">
                Priority
              </label>
              <select
                id="priority"
                value={newTodo.priority}
                onChange={(e) => setNewTodo({...newTodo, priority: e.target.value})}
                className="relative block w-full px-4 py-3 border border-cyan-500/50 text-white bg-black/30 backdrop-blur-md rounded-xl focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-500/50 focus:shadow-[0_0_20px_rgba(6,182,212,0.4)] focus:z-10 transition-all duration-300 hover:border-cyan-400/70 font-mono"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>
            <button
              type="submit"
              className="w-full flex justify-center py-4 px-4 border border-emerald-500/50 text-lg font-semibold rounded-xl text-white bg-gradient-to-r from-emerald-600 via-teal-500 to-emerald-600 hover:from-emerald-700 hover:via-teal-600 hover:to-emerald-700 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 transition-all duration-300 hover:scale-[1.02] transform hover:shadow-lg hover:shadow-emerald-500/30 font-mono"
            >
              Add Todo
            </button>
          </form>
        </motion.div>

        {/* Todo List - Glassmorphism Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white/5 backdrop-blur-xl rounded-2xl overflow-hidden border border-cyan-500/30 shadow-2xl shadow-cyan-500/20"
        >
          <div className="px-6 py-6 border-b border-cyan-500/30">
            <h2 className="text-xl font-semibold font-mono bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">Your Todos ({todos.length})</h2>
          </div>

          {todos.length === 0 ? (
            <div className="p-12 text-center">
              <p className="text-gray-400 text-lg font-mono">No todos yet. Add one above!</p>
            </div>
          ) : (
            <ul className="divide-y divide-cyan-500/20">
              <AnimatePresence>
                {todos.map((todo) => (
                  <motion.li
                    key={todo.id}
                    layout
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    transition={{ duration: 0.3 }}
                    className="px-6 py-6 hover:bg-white/5 transition-colors duration-300 border-b border-cyan-500/10 last:border-0"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <input
                          type="checkbox"
                          checked={todo.completed}
                          onChange={() => toggleTodo(todo.id, todo.completed)}
                          className="h-5 w-5 text-emerald-500 focus:ring-cyan-500 border-cyan-500/50 rounded bg-black/30 backdrop-blur-md cursor-pointer"
                        />
                        <span className={`ml-4 text-base font-mono ${todo.completed ? 'line-through text-gray-500' : 'text-white'}`}>
                          {todo.title}
                        </span>
                        <span className={`ml-4 px-2 py-1 rounded-full text-xs font-bold ${
                          todo.priority === 'high'
                            ? 'bg-red-500/30 text-red-300 border border-red-500/50 shadow-sm shadow-red-500/30'
                            : todo.priority === 'medium'
                              ? 'bg-yellow-500/30 text-yellow-300 border border-yellow-500/50 shadow-sm shadow-yellow-500/30'
                              : 'bg-green-500/30 text-green-300 border border-green-500/50 shadow-sm shadow-green-500/30'
                        }`}>
                          {todo.priority.toUpperCase()}
                        </span>
                      </div>
                      <div className="flex space-x-3">
                        <button
                          onClick={() => deleteTodo(todo.id)}
                          className="inline-flex items-center px-4 py-2 border border-red-500/50 text-sm font-medium rounded-lg text-red-400 bg-red-900/30 hover:bg-red-900/50 focus:outline-none focus:ring-2 focus:ring-red-500/50 transition-all duration-300 hover:shadow-lg hover:shadow-red-500/30 font-mono"
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                    {todo.description && (
                      <div className="ml-9 mt-2 text-sm text-gray-400 font-mono">
                        {todo.description}
                      </div>
                    )}
                    <div className="ml-9 mt-2 text-xs text-gray-500 font-mono">
                      Created: {new Date(todo.created_at).toLocaleString()}
                    </div>
                  </motion.li>
                ))}
              </AnimatePresence>
            </ul>
          )}
        </motion.div>
      </main>
    </div>
  );
}