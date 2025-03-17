import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { supabase } from '../lib/supabase';
import { scoreResume } from '../lib/resumeScoring';
import toast from 'react-hot-toast';

export default function ApplicationForm() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    email: '',
    resume: null as File | null,
  });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    try {
      const user = (await supabase.auth.getUser()).data.user;
      if (!user) throw new Error('Not authenticated');

      if (!formData.resume) {
        throw new Error('Please upload a resume');
      }

      // Upload resume to Supabase Storage
      const { data: fileData, error: uploadError } = await supabase.storage
        .from('resumes')
        .upload(`${user.id}/${formData.resume.name}`, formData.resume);

      if (uploadError) throw uploadError;

      // Score the resume
      const resumeScore = await scoreResume(fileData.path);

      // Create application record
      const { error: applicationError } = await supabase
        .from('applications')
        .insert({
          user_id: user.id,
          name: formData.name,
          phone: formData.phone,
          email: formData.email,
          resume_url: fileData.path,
          resume_score: resumeScore
        });

      if (applicationError) throw applicationError;

      toast.success('Application submitted successfully!');
      navigate('/waiting-room');
    } catch (error) {
      toast.error(error.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md mx-auto">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <h2 className="text-2xl font-bold mb-8 text-center text-gray-900">
            Submit Your Application
          </h2>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                Full Name
              </label>
              <input
                type="text"
                id="name"
                required
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                value={formData.name}
                onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
              />
            </div>

            <div>
              <label htmlFor="phone" className="block text-sm font-medium text-gray-700">
                Phone Number
              </label>
              <input
                type="tel"
                id="phone"
                required
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                value={formData.phone}
                onChange={(e) => setFormData(prev => ({ ...prev, phone: e.target.value }))}
              />
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Email
              </label>
              <input
                type="email"
                id="email"
                required
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                value={formData.email}
                onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))}
              />
            </div>

            <div>
              <label htmlFor="resume" className="block text-sm font-medium text-gray-700">
                Resume (PDF)
              </label>
              <input
                type="file"
                id="resume"
                accept=".pdf"
                required
                className="mt-1 block w-full"
                onChange={(e) => setFormData(prev => ({ ...prev, resume: e.target.files?.[0] || null }))}
              />
              <p className="mt-1 text-sm text-gray-500">
                Upload your resume in PDF format. Include GitHub links for better scoring.
              </p>
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white ${
                isSubmitting 
                  ? 'bg-blue-400 cursor-not-allowed' 
                  : 'bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500'
              }`}
            >
              {isSubmitting ? 'Submitting...' : 'Submit Application'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}