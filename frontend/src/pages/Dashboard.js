import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

function Dashboard({ user }) {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await axios.get('/api/stats');
      setStats(response.data);
    } catch (err) {
      console.error('Error fetching stats:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <h2 style={{color: 'white', marginBottom: '2rem'}}>
        Welcome back, {user.name}! 👋
      </h2>

      {!user.has_face_data && (
        <div className="message message-info" style={{marginBottom: '2rem'}}>
          <strong>Action Required:</strong> You haven't enrolled your face yet. 
          <Link to="/enroll-face" style={{marginLeft: '0.5rem', fontWeight: 'bold'}}>
            Enroll now
          </Link> to appear in photos automatically.
        </div>
      )}

      {stats && (
        <div className="stats-grid">
          <div className="stat-card">
            <h2>{stats.total_users}</h2>
            <p>Total Users</p>
          </div>
          <div className="stat-card">
            <h2>{stats.total_photos}</h2>
            <p>Total Photos</p>
          </div>
          <div className="stat-card">
            <h2>{stats.processed_photos}</h2>
            <p>Processed</p>
          </div>
          <div className="stat-card">
            <h2>{stats.pending_photos}</h2>
            <p>Pending</p>
          </div>
        </div>
      )}

      <div className="dashboard-grid">
        <Link to="/my-photos" className="dashboard-card">
          <h3>🖼️ My Photos</h3>
          <p>View all photos where you appear. Browse and download your pictures from events.</p>
        </Link>

        <Link to="/upload" className="dashboard-card">
          <h3>📤 Upload Photos</h3>
          <p>Upload photos from your latest event. Our AI will automatically detect and tag everyone.</p>
        </Link>

        <Link to="/enroll-face" className="dashboard-card">
          <h3>👤 {user.has_face_data ? 'Update' : 'Enroll'} Face</h3>
          <p>
            {user.has_face_data 
              ? 'Update your face data with new photos for better recognition.'
              : 'Register your face so you can be identified in photos automatically.'}
          </p>
        </Link>

        <div className="dashboard-card" style={{opacity: 0.6, cursor: 'not-allowed'}}>
          <h3>⚙️ Settings</h3>
          <p>Manage your account, privacy settings, and preferences. (Coming Soon)</p>
        </div>
      </div>

      <div style={{background: 'white', borderRadius: '12px', padding: '2rem', marginTop: '2rem'}}>
        <h3>How It Works</h3>
        <ol style={{lineHeight: '2'}}>
          <li><strong>Enroll Your Face:</strong> Upload 3-5 photos of yourself so our AI can recognize you.</li>
          <li><strong>Upload Event Photos:</strong> After any event, upload all photos in bulk.</li>
          <li><strong>Automatic Detection:</strong> Our AI identifies everyone in the photos.</li>
          <li><strong>Personalized Gallery:</strong> Each person gets their own gallery with only photos they appear in.</li>
        </ol>
      </div>
    </div>
  );
}

export default Dashboard;
