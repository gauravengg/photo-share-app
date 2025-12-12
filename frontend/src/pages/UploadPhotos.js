import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function UploadPhotos({ user }) {
  const [files, setFiles] = useState([]);
  const [eventName, setEventName] = useState('');
  const [uploading, setUploading] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleFileSelect = (e) => {
    const selectedFiles = Array.from(e.target.files);
    setFiles(selectedFiles);
    setError('');
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    
    if (files.length === 0) {
      setError('Please select photos to upload');
      return;
    }

    setUploading(true);
    setError('');
    setMessage('');

    const formData = new FormData();
    files.forEach(file => {
      formData.append('files', file);
    });
    formData.append('uploaded_by', user.user_id);
    if (eventName) {
      formData.append('event_name', eventName);
    }

    try {
      const uploadResponse = await axios.post('/api/upload-photos', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setMessage(`✅ Uploaded ${uploadResponse.data.photo_ids.length} photos successfully!`);
      setUploading(false);
      
      // Now process the photos
      setProcessing(true);
      setMessage('✅ Upload complete! Now processing photos...');
      
      const processResponse = await axios.post('/api/process-photos');
      
      setMessage(`✅ Successfully processed ${processResponse.data.processed_count} photos! Redirecting...`);
      setProcessing(false);
      
      // Reset form
      setFiles([]);
      setEventName('');
      
      // Redirect to my photos after 2 seconds
      setTimeout(() => {
        navigate('/my-photos');
      }, 2000);

    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed. Please try again.');
      setUploading(false);
      setProcessing(false);
    }
  };

  return (
    <div className="container">
      <div className="page-container" style={{maxWidth: '800px'}}>
        <h2>📤 Upload Event Photos</h2>
        
        <div className="message message-info">
          Upload all photos from your event. Our AI will automatically detect and identify everyone!
        </div>

        {error && <div className="message message-error">{error}</div>}
        {message && <div className="message message-success">{message}</div>}

        <form onSubmit={handleUpload}>
          <div className="form-group">
            <label>Event Name (Optional)</label>
            <input
              type="text"
              value={eventName}
              onChange={(e) => setEventName(e.target.value)}
              placeholder="e.g., Company Picnic 2024, Birthday Party"
            />
          </div>

          <div className="file-upload" onClick={() => document.getElementById('photo-upload').click()}>
            <input
              id="photo-upload"
              type="file"
              accept="image/*"
              multiple
              onChange={handleFileSelect}
            />
            <p style={{fontSize: '3rem', margin: '0'}}>📁</p>
            <p>Click to select photos</p>
            <p style={{fontSize: '0.9rem', color: '#666'}}>
              {files.length > 0 ? `${files.length} photo(s) selected` : 'No files selected'}
            </p>
          </div>

          {files.length > 0 && (
            <div style={{marginTop: '1rem', padding: '1rem', background: '#f8f9fa', borderRadius: '8px'}}>
              <h4>Selected Photos:</h4>
              <ul style={{maxHeight: '200px', overflowY: 'auto'}}>
                {files.map((file, index) => (
                  <li key={index}>{file.name}</li>
                ))}
              </ul>
            </div>
          )}

          <button 
            type="submit" 
            className="btn btn-primary" 
            disabled={uploading || processing || files.length === 0}
            style={{width: '100%', marginTop: '1.5rem'}}
          >
            {uploading ? 'Uploading...' : processing ? 'Processing Photos...' : 'Upload & Process'}
          </button>
        </form>

        <div style={{marginTop: '2rem', padding: '1rem', background: '#f8f9fa', borderRadius: '8px'}}>
          <h4>💡 Tips:</h4>
          <ul style={{lineHeight: '1.8'}}>
            <li>Upload all photos at once for faster processing</li>
            <li>Supported formats: JPG, PNG, GIF</li>
            <li>Processing time depends on number of photos and faces</li>
            <li>Make sure all participants have enrolled their faces first</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default UploadPhotos;
