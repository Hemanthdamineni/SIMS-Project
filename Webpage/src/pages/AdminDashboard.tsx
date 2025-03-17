import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { supabase } from '../lib/supabase';
import { Download, CheckCircle, XCircle, TrendingUp } from 'lucide-react';
import toast from 'react-hot-toast';

export default function AdminDashboard() {
  const navigate = useNavigate();
  const [applications, setApplications] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAdmin = async () => {
      const user = (await supabase.auth.getUser()).data.user;
      if (!user?.email?.endsWith('@admin.com')) {
        navigate('/login');
        return;
      }
    };

    const fetchApplications = async () => {
      const { data, error } = await supabase
        .from('applications')
        .select('*')
        .order('created_at', { ascending: false });

      if (error) {
        toast.error('Failed to fetch applications');
        return;
      }

      setApplications(data || []);
      setLoading(false);
    };

    checkAdmin();
    fetchApplications();
  }, [navigate]);

  const handleDownload = async (resumeUrl: string) => {
    try {
      const { data, error } = await supabase.storage
        .from('resumes')
        .download(resumeUrl);

      if (error) throw error;

      const url = URL.createObjectURL(data);
      const a = document.createElement('a');
      a.href = url;
      a.download = resumeUrl.split('/').pop() || 'resume.pdf';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (error) {
      toast.error('Failed to download resume');
    }
  };

  const handleStatusUpdate = async (id: string, status: 'accepted' | 'rejected') => {
    try {
      const { error } = await supabase
        .from('applications')
        .update({ status })
        .eq('id', id);

      if (error) throw error;

      setApplications(prev =>
        prev.map(app =>
          app.id === id ? { ...app, status } : app
        )
      );

      toast.success(`Application ${status} successfully`);
    } catch (error) {
      toast.error('Failed to update application status');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Applications Dashboard</h1>
        
        <div className="bg-white shadow-md rounded-lg overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Applicant
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Contact
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Resume Score
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {applications.map((application) => (
                <tr key={application.id}>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">{application.name}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">{application.email}</div>
                    <div className="text-sm text-gray-500">{application.phone}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <TrendingUp className={`h-5 w-5 mr-2 ${
                        application.resume_score >= 70 ? 'text-green-500' :
                        application.resume_score >= 40 ? 'text-yellow-500' :
                        'text-red-500'
                      }`} />
                      <span className="text-sm text-gray-900">{application.resume_score}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                      application.status === 'accepted' ? 'bg-green-100 text-green-800' :
                      application.status === 'rejected' ? 'bg-red-100 text-red-800' :
                      'bg-yellow-100 text-yellow-800'
                    }`}>
                      {application.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                    <button
                      onClick={() => handleDownload(application.resume_url)}
                      className="text-blue-600 hover:text-blue-900"
                      title="Download Resume"
                    >
                      <Download className="h-5 w-5" />
                    </button>
                    <button
                      onClick={() => handleStatusUpdate(application.id, 'accepted')}
                      className={`text-green-600 hover:text-green-900 ${
                        application.status !== 'pending' ? 'opacity-50 cursor-not-allowed' : ''
                      }`}
                      disabled={application.status !== 'pending'}
                      title="Accept Application"
                    >
                      <CheckCircle className="h-5 w-5" />
                    </button>
                    <button
                      onClick={() => handleStatusUpdate(application.id, 'rejected')}
                      className={`text-red-600 hover:text-red-900 ${
                        application.status !== 'pending' ? 'opacity-50 cursor-not-allowed' : ''
                      }`}
                      disabled={application.status !== 'pending'}
                      title="Reject Application"
                    >
                      <XCircle className="h-5 w-5" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}