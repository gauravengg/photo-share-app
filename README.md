# Smart Photo Share - MVP Setup

## Project Overview
Automatically identify people in photos and share images with the right individuals using facial recognition.

## Tech Stack
- **Backend**: Python (FastAPI)
- **Face Recognition**: face_recognition library (dlib-based)
- **Database**: PostgreSQL with pgvector for face embeddings
- **Storage**: Local filesystem (can migrate to S3 later)
- **Frontend**: React (simple web interface)

## Team Allocation (2 people)

### Person 1: Backend + ML Pipeline
- Face detection and recognition
- API endpoints
- Database setup
- Photo processing pipeline

### Person 2: Frontend + Integration
- React UI for upload/view
- User authentication
- Integration with backend APIs
- Testing and bug fixes

## Project Timeline (3 weeks MVP)

### Week 1: Core Foundation
- Day 1-2: Project setup, database schema, basic API structure
- Day 3-4: Face detection and embedding generation
- Day 5-7: Face matching and photo tagging logic

### Week 2: Features
- Day 8-10: User registration and face enrollment
- Day 11-12: Bulk photo upload and processing
- Day 13-14: Photo gallery and sharing logic

### Week 3: Polish
- Day 15-17: UI improvements, error handling
- Day 18-19: Testing with real data
- Day 20-21: Deploy and gather feedback

## Quick Start

### Prerequisites
```bash
# Python 3.9+
# Node.js 16+
# PostgreSQL 14+
```

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
python main.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## Project Structure
```
photo-share-app/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── models.py            # Database models
│   ├── face_recognition.py  # Face detection/matching
│   ├── utils.py             # Helper functions
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.js
│   └── package.json
└── uploads/                 # Photo storage
    ├── originals/
    └── faces/
```

## MVP Features (Must Have)
1. ✅ User registration with face enrollment (3-5 photos per person)
2. ✅ Bulk photo upload
3. ✅ Automatic face detection and matching
4. ✅ Per-user photo gallery (only photos they appear in)
5. ✅ Simple sharing via unique links

## Features to Skip for MVP
- ❌ Social features (likes, comments)
- ❌ Advanced editing tools
- ❌ Mobile apps (web-first)
- ❌ Payment integration
- ❌ Email notifications (manual share for now)

## Success Metrics for MVP
- 90%+ face detection rate
- 85%+ face matching accuracy
- < 5 seconds per photo processing
- Successfully tested with 20+ people, 100+ photos

## Next Steps After MVP
1. Deploy to cloud (AWS/Railway)
2. Add email notifications
3. Improve UI/UX based on feedback
4. Add privacy controls
5. Consider mobile app
