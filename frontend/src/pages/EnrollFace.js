import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function EnrollFace({ user }) {
  const [files, setFiles] = useState([]);
  const [previews, setPreviews] = useState([]);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleFileSelect = (e) => {
    const selectedFiles = Array.from(e.target.files);
    
    if (selectedFiles.length < 3) {
      setError('Please select at least 3 photos of yourself');
      return;
    }

    if (selectedFiles.length > 5) {
      setError('Maximum 5 photos allowed');
      return;
    }

    setFiles(selectedFiles);
    setError('');

    // Create previews
    const filePreviews = selectedFiles.map(file => URL.createObjectURL(file));
    setPreviews(filePreviews);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (files.length < 3) {
      setError('Please select at least 3 photos');
      return;
    }

    setLoading(true);
    setError('');
    setMessage('');

    const formData = new FormData();
    files.forEach(file => {
      formData.append('files', file);
    });

    try {
      const response = await axios.post(
        `/api/enroll-face/${user.user_id}`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      setMessage(`Success! ${response.data.enrolled_count} face samples enrolled.`);
      
      // Update user data
      const updatedUser = { ...user, has_face_data: true };
      localStorage.setItem('user', JSON.stringify(updatedUser));

      // Redirect to dashboard after 2 seconds
      setTimeout(() => {
        navigate('/dashboard');
      }, 2000);

    } catch (err) {
      setError(err.response?.data?.detail || 'Face enrollment failed. Make sure your face is clearly visible.');
    } finally {
      setLoading(false);
    }
  };

  const handleSkip = () => {
    navigate('/dashboard');
  };

  return (
    <div className="page-container">
      <h2>📸 Enroll Your Face</h2>
      
      <div className="message message-info">
        <strong>Important:</strong> Upload 3-5 clear photos of yourself for best results. 
        Make sure your face is clearly visible and well-lit.
      </div>

      {error && <div className="message message-error">{error}</div>}
      {message && <div className="message message-success">{message}</div>}

      <form onSubmit={handleSubmit}>
        <div className="file-upload" onClick={() => document.getElementById('face-upload').click()}>
          <input
            id="face-upload"
            type="file"
            accept="image/*"
            multiple
            onChange={handleFileSelect}
          />
          <p style={{fontSize: '3rem', margin: '0'}}>📷</p>
          <p>Click to select 3-5 photos of yourself</p>
          <p style={{fontSize: '0.9rem', color: '#666'}}>
            {files.length > 0 ? `${files.length} photo(s) selected` : 'No files selected'}
          </p>
        </div>

        {previews.length > 0 && (
          <div className="photo-grid" style={{marginTop: '1.5rem'}}>
            {previews.map((preview, index) => (
              <div key={index} className="photo-item">
                <img src={preview} alt={`Preview ${index + 1}`} />
              </div>
            ))}
          </div>
        )}

        <div style={{marginTop: '1.5rem', display: 'flex', gap: '1rem'}}>
          <button 
            type="submit" 
            className="btn btn-primary" 
            disabled={loading || files.length < 3}
            style={{flex: 1}}
          >
            {loading ? 'Processing...' : 'Enroll Face'}
          </button>
          <button 
            type="button" 
            className="btn btn-secondary" 
            onClick={handleSkip}
            style={{flex: 1}}
          >
            Skip for Now
          </button>
        </div>
      </form>

      <div style={{marginTop: '2rem', padding: '1rem', background: '#f8f9fa', borderRadius: '8px'}}>
        <h4>Tips for good photos:</h4>
        <ul style={{lineHeight: '1.8'}}>
          <li>Face should be clearly visible</li>
          <li>Good lighting (avoid shadows)</li>
          <li>Different angles (front, slight side views)</li>
          <li>Natural expressions</li>
          <li>No sunglasses or face coverings</li>
        </ul>
      </div>
    </div>
  );
}

export default EnrollFace;
