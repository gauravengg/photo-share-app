import React, { useState, useEffect } from 'react';
import axios from 'axios';

function MyPhotos({ user }) {
  const [photos, setPhotos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedPhoto, setSelectedPhoto] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchMyPhotos();
  }, [user.user_id]);

  const fetchMyPhotos = async () => {
    try {
      const response = await axios.get(`/api/my-photos/${user.user_id}`);
      setPhotos(response.data.photos);
    } catch (err) {
      setError('Failed to load photos');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handlePhotoClick = (photo) => {
    setSelectedPhoto(photo);
  };

  const closeModal = () => {
    setSelectedPhoto(null);
  };

  const downloadPhoto = async (photoId) => {
    try {
      const response = await axios.get(`/api/photo/${photoId}`, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `photo_${photoId}.jpg`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error('Download failed:', err);
    }
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading your photos...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div style={{background: 'white', borderRadius: '12px', padding: '2rem'}}>
        <h2>🖼️ My Photos</h2>
        
        {error && <div className="message message-error">{error}</div>}

        {!user.has_face_data && (
          <div className="message message-info">
            You haven't enrolled your face yet. Photos where you appear will show up here once you enroll.
          </div>
        )}

        {photos.length === 0 ? (
          <div style={{textAlign: 'center', padding: '3rem', color: '#666'}}>
            <p style={{fontSize: '3rem'}}>📷</p>
            <h3>No photos yet</h3>
            <p>Photos where you appear will show up here automatically.</p>
            {user.has_face_data && (
              <p>Make sure someone uploads photos from events you attended!</p>
            )}
          </div>
        ) : (
          <>
            <p style={{color: '#666', marginBottom: '1.5rem'}}>
              Found {photos.length} photo{photos.length !== 1 ? 's' : ''} with you in them
            </p>

            <div className="photo-grid">
              {photos.map((photo) => (
                <div 
                  key={photo.id} 
                  className="photo-item"
                  onClick={() => handlePhotoClick(photo)}
                >
                  <img 
                    src={`/api/thumbnail/${photo.id}`} 
                    alt={`Photo ${photo.id}`}
                    onError={(e) => {
                      e.target.src = 'https://via.placeholder.com/200?text=Image+Not+Found';
                    }}
                  />
                  {photo.event_name && (
                    <div style={{
                      position: 'absolute',
                      bottom: 0,
                      left: 0,
                      right: 0,
                      background: 'rgba(0,0,0,0.7)',
                      color: 'white',
                      padding: '0.5rem',
                      fontSize: '0.85rem'
                    }}>
                      {photo.event_name}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </>
        )}
      </div>

      {/* Photo Modal */}
      {selectedPhoto && (
        <div 
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'rgba(0,0,0,0.9)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000,
            padding: '2rem'
          }}
          onClick={closeModal}
        >
          <div 
            style={{
              position: 'relative',
              maxWidth: '90%',
              maxHeight: '90%'
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <button
              onClick={closeModal}
              style={{
                position: 'absolute',
                top: '-40px',
                right: '0',
                background: 'white',
                border: 'none',
                padding: '0.5rem 1rem',
                borderRadius: '4px',
                cursor: 'pointer',
                fontSize: '1.2rem'
              }}
            >
              ✕
            </button>
            
            <img 
              src={`/api/photo/${selectedPhoto.id}`}
              alt={`Photo ${selectedPhoto.id}`}
              style={{
                maxWidth: '100%',
                maxHeight: '80vh',
                borderRadius: '8px'
              }}
            />
            
            <button
              onClick={() => downloadPhoto(selectedPhoto.id)}
              className="btn btn-primary"
              style={{
                position: 'absolute',
                bottom: '-50px',
                left: '50%',
                transform: 'translateX(-50%)',
                whiteSpace: 'nowrap'
              }}
            >
              📥 Download
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default MyPhotos;
