import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Building2, LogIn } from 'lucide-react';
import { supabase } from '../lib/supabase';

export default function Navbar() {
  const navigate = useNavigate();
  const [user, setUser] = React.useState(null);

  React.useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null);
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null);
    });

    return () => subscription.unsubscribe();
  }, []);

  const handleLogout = async () => {
    await supabase.auth.signOut();
    navigate('/');
  };

  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center">
              <Building2 className="h-8 w-8 text-blue-600" />
              <span className="ml-2 text-xl font-bold text-gray-800">SIMS</span>
            </Link>
            <div className="hidden md:flex items-center space-x-4 ml-10">
              <Link to="/" className="text-gray-600 hover:text-gray-900 px-3 py-2">Home</Link>
              <Link to="/about" className="text-gray-600 hover:text-gray-900 px-3 py-2">About</Link>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            {user ? (
              <>
                <span className="text-gray-600">{user.email}</span>
                <button
                  onClick={handleLogout}
                  className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="flex items-center text-gray-600 hover:text-gray-900"
                >
                  <LogIn className="h-5 w-5 mr-1" />
                  Login
                </Link>
                <Link
                  to="/admin/login"
                  className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                >
                  Admin Login
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}