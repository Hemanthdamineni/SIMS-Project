import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { supabase } from '../lib/supabase';
import { Clock } from 'lucide-react';

export default function WaitingRoom() {
  const navigate = useNavigate();
  const [application, setApplication] = useState<any>(null);

  useEffect(() => {
    const fetchApplication = async () => {
      const user = (await supabase.auth.getUser()).data.user;
      if (!user) {
        navigate('/login');
        return;
      }

      const { data, error } = await supabase
        .from('applications')
        .select('*')
        .eq('user_id', user.id)
        .single();

      if (error) {
        navigate('/apply');
        return;
      }

      setApplication(data);
    };

    fetchApplication();

    // Subscribe to changes
    const subscription = supabase
      .channel('application_updates')
      .on('postgres_changes', {
        event: 'UPDATE',
        schema: 'public',
        table: 'applications',
        filter: `user_id=eq.${(supabase.auth.getUser()).data?.user?.id}`,
      }, 
      (payload) => {
        setApplication(payload.new);
      })
      .subscribe();

    return () => {
      subscription.unsubscribe();
    };
  }, [navigate]);

  if (!application) {
    return <div>Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 bg-white p-8 rounded-lg shadow-md">
        <div className="text-center">
          <Clock className="mx-auto h-12 w-12 text-blue-600" />
          <h2 className="mt-6 text-3xl font-extrabold text-gray-900">
            Application Status
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Your application is being reviewed by our team
          </p>
        </div>

        <div className="mt-8">
          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-medium text-gray-900">Status</h3>
              <p className={`mt-1 text-sm ${
                application.status === 'accepted' ? 'text-green-600' :
                application.status === 'rejected' ? 'text-red-600' :
                'text-yellow-600'
              }`}>
                {application.status.charAt(0).toUpperCase() + application.status.slice(1)}
              </p>
            </div>

            <div>
              <h3 className="text-lg font-medium text-gray-900">Submitted Details</h3>
              <div className="mt-2 text-sm text-gray-600">
                <p>Name: {application.name}</p>
                <p>Email: {application.email}</p>
                <p>Phone: {application.phone}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}