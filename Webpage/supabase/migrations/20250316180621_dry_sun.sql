/*
  # Create applications table

  1. New Tables
    - `applications`
      - `id` (uuid, primary key)
      - `user_id` (uuid, references auth.users)
      - `name` (text)
      - `phone` (text)
      - `email` (text)
      - `resume_url` (text)
      - `status` (text) - can be 'pending', 'accepted', or 'rejected'
      - `resume_score` (integer)
      - `created_at` (timestamp)

  2. Security
    - Enable RLS on `applications` table
    - Add policies for users to read/create their own applications
    - Add policies for admins to read/update all applications
*/

-- Create applications table
CREATE TABLE IF NOT EXISTS applications (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES auth.users NOT NULL,
  name text NOT NULL,
  phone text NOT NULL,
  email text NOT NULL,
  resume_url text NOT NULL,
  status text DEFAULT 'pending',
  resume_score integer DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

-- Enable RLS
ALTER TABLE applications ENABLE ROW LEVEL SECURITY;

-- Policies for regular users
CREATE POLICY "Users can create their own applications"
  ON applications
  FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can read their own applications"
  ON applications
  FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

-- Policies for admins (assuming admin role)
CREATE POLICY "Admins can read all applications"
  ON applications
  FOR SELECT
  TO authenticated
  USING (EXISTS (
    SELECT 1 FROM auth.users
    WHERE auth.users.id = auth.uid()
    AND auth.users.email LIKE '%@admin.com'
  ));

CREATE POLICY "Admins can update applications"
  ON applications
  FOR UPDATE
  TO authenticated
  USING (EXISTS (
    SELECT 1 FROM auth.users
    WHERE auth.users.id = auth.uid()
    AND auth.users.email LIKE '%@admin.com'
  ));