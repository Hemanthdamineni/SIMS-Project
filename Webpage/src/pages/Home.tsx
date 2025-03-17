import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Building2, FileText, Users, Clock } from 'lucide-react';
import { supabase } from '../lib/supabase';

export default function Home() {
  const navigate = useNavigate();
  const [user, setUser] = React.useState<any>(null);

  React.useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null);
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null);
    });

    return () => subscription.unsubscribe();
  }, []);

  const handleApplyClick = () => {
    if (!user) {
      toast.error('Please login to submit an application');
      navigate('/login');
      return;
    }
    navigate('/apply');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <Building2 className="mx-auto h-16 w-16 text-blue-600" />
          <h1 className="mt-4 text-4xl font-bold text-gray-900">Welcome to SIMS</h1>
          <p className="mt-2 text-lg text-gray-600">
            Your Comprehensive Staffing Information Management System
          </p>
          {user && (
            <button
              onClick={handleApplyClick}
              className="mt-8 inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
            >
              <FileText className="mr-2 h-5 w-5" />
              Submit Application
            </button>
          )}
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="flex items-center mb-4">
              <Building2 className="h-6 w-6 text-blue-600 mr-2" />
              <h2 className="text-xl font-semibold text-gray-900">Company Motto</h2>
            </div>
            <p className="text-gray-600">
              Empowering businesses through efficient staffing solutions. We connect talented individuals with outstanding opportunities.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="flex items-center mb-4">
              <Users className="h-6 w-6 text-green-600 mr-2" />
              <h2 className="text-xl font-semibold text-gray-900">Job Listings</h2>
            </div>
            <p className="text-gray-600">
              Explore exciting career opportunities with leading companies. We offer positions across various industries and skill levels.
            </p>
            <Link
              to="/jobs"
              className="mt-4 inline-flex items-center text-blue-600 hover:text-blue-800"
            >
              View Opportunities →
            </Link>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="flex items-center mb-4">
              <Clock className="h-6 w-6 text-purple-600 mr-2" />
              <h2 className="text-xl font-semibold text-gray-900">Application Process</h2>
            </div>
            <p className="text-gray-600">
              Simple 3-step process: Sign up, submit your application, and track your status in real-time through our waiting room.
            </p>
          </div>
        </div>

        {/* How It Works Section */}
        <div className="bg-white rounded-lg shadow-md p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">How It Works</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="flex flex-col items-center">
              <div className="bg-blue-100 rounded-full p-3 mb-4">
                <Users className="h-6 w-6 text-blue-600" />
              </div>
              <h3 className="text-lg font-semibold mb-2">1. Create Account</h3>
              <p className="text-center text-gray-600">
                Sign up with your email to get started with our application process.
              </p>
            </div>
            
            <div className="flex flex-col items-center">
              <div className="bg-green-100 rounded-full p-3 mb-4">
                <FileText className="h-6 w-6 text-green-600" />
              </div>
              <h3 className="text-lg font-semibold mb-2">2. Submit Application</h3>
              <p className="text-center text-gray-600">
                Fill out your details and upload your resume with relevant experience.
              </p>
            </div>

            <div className="flex flex-col items-center">
              <div className="bg-purple-100 rounded-full p-3 mb-4">
                <Clock className="h-6 w-6 text-purple-600" />
              </div>
              <h3 className="text-lg font-semibold mb-2">3. Track Status</h3>
              <p className="text-center text-gray-600">
                Monitor your application status in real-time through our waiting room.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}