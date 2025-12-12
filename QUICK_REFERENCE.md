# 📋 Quick Reference Card

## 🚀 Starting the Application

### Backend (Terminal 1)
```bash
cd photo-share-app/backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python main.py
```
**URL:** http://localhost:8000
**API Docs:** http://localhost:8000/docs

### Frontend (Terminal 2)
```bash
cd photo-share-app/frontend
npm start
```
**URL:** http://localhost:3000

---

## 🔧 Common Commands

### Backend
```bash
# Create new database
python init_db.py

# Install new package
pip install package-name
pip freeze > requirements.txt

# Run tests (if you add tests)
pytest

# Check database
sqlite3 photo_share.db
```

### Frontend
```bash
# Install new package
npm install package-name

# Build for production
npm run build

# Check for errors
npm run lint
```

---

## 📁 Key Files to Know

### Backend
- `main.py` - All API routes
- `models.py` - Database schema
- `face_recognition_service.py` - Face detection logic

### Frontend
- `src/App.js` - Main component & routing
- `src/pages/*.js` - All page components
- `src/App.css` - Styling

---

## 🐛 Debugging Tips

### Backend Not Starting?
1. Check if port 8000 is free: `lsof -ti:8000`
2. Activate virtual environment
3. Check for Python errors in terminal

### Frontend Not Starting?
1. Check if port 3000 is free: `lsof -ti:3000`
2. Delete node_modules and reinstall: `rm -rf node_modules && npm install`
3. Check browser console (F12)

### Face Recognition Not Working?
1. Check photo quality (clear, well-lit)
2. Verify face_recognition installed: `pip list | grep face-recognition`
3. Check backend logs for errors

### Photos Not Appearing?
1. Check if processing completed: GET `/api/stats`
2. Verify user enrolled face: Check `has_face_data`
3. Check uploads directory permissions

---

## 🔌 API Endpoints Quick Reference

### User Management
- `POST /api/register` - Register new user
- `POST /api/login` - Login user

### Face Enrollment
- `POST /api/enroll-face/{user_id}` - Upload face photos

### Photo Management
- `POST /api/upload-photos` - Upload event photos
- `POST /api/process-photos` - Process pending photos
- `GET /api/my-photos/{user_id}` - Get user's photos
- `GET /api/photo/{photo_id}` - Get full photo
- `GET /api/thumbnail/{photo_id}` - Get thumbnail

### Stats
- `GET /api/stats` - System statistics

---

## 📊 Database Schema

```
Person
├── id
├── name
├── email
├── password_hash
└── face_embeddings (JSON)

Photo
├── id
├── file_path
├── thumbnail_path
├── uploaded_by
├── processed (0=pending, 1=done, -1=failed)
└── event_name

photo_person (many-to-many)
├── photo_id
├── person_id
└── confidence
```

---

## 🎨 UI Pages

1. **Login** (`/login`) - User authentication
2. **Register** (`/register`) - New user signup
3. **Dashboard** (`/dashboard`) - Main overview
4. **Enroll Face** (`/enroll-face`) - Face registration
5. **Upload Photos** (`/upload`) - Bulk photo upload
6. **My Photos** (`/my-photos`) - Personal gallery

---

## 🧪 Test Data

### Test Users
Create 3-4 test users with different photos:
```
User 1: alice@test.com / password123
User 2: bob@test.com / password123
User 3: charlie@test.com / password123
```

### Test Photos
1. Get 5-10 individual photos (for enrollment)
2. Get 10-20 group photos (for testing)
3. Ensure good lighting and clear faces

---

## 📈 Performance Benchmarks

**Target Metrics:**
- Face detection: < 2 sec per photo
- Face matching: < 1 sec per face
- Photo upload: < 5 sec for 10 photos
- Page load: < 2 sec

**Current Setup:**
- Local SQLite database
- Local file storage
- Single-threaded processing

**For Production:**
- PostgreSQL database
- AWS S3 storage
- Background job queue (Celery)
- Redis caching

---

## 🔐 Security Notes

**Current (Development):**
- Simple password hashing (bcrypt)
- No JWT tokens (session-based)
- No rate limiting
- Local storage only

**TODO for Production:**
- Add JWT authentication
- Implement rate limiting
- Add CSRF protection
- Use HTTPS only
- Environment-based secrets

---

## 📝 Commit Message Template

```
feat: Add user authentication
fix: Resolve face detection issue
docs: Update API documentation
style: Improve dashboard layout
refactor: Optimize photo processing
test: Add unit tests for face matching
chore: Update dependencies
```

---

## 🆘 Emergency Commands

### Stop Everything
```bash
# Kill backend
pkill -f "python main.py"

# Kill frontend
pkill -f "react-scripts"
```

### Reset Database
```bash
cd backend
rm photo_share.db
python init_db.py
```

### Clear All Photos
```bash
rm -rf uploads/*
mkdir -p uploads/{originals,faces,thumbnails}
```

### Fresh Install
```bash
# Backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 📞 Getting Help

**Backend Issues:**
- Check FastAPI docs: https://fastapi.tiangolo.com/
- face_recognition issues: https://github.com/ageitgey/face_recognition/issues

**Frontend Issues:**
- React docs: https://react.dev/
- Stack Overflow: Tag with `reactjs` and `fastapi`

**Both:**
- Check terminal/console for errors
- Read the error message carefully
- Google the exact error message
- Ask your teammate!

---

## ✅ Pre-Launch Checklist

- [ ] All features working locally
- [ ] No console errors
- [ ] Tested with 3+ users
- [ ] Tested with 50+ photos
- [ ] Mobile responsive
- [ ] Privacy policy added
- [ ] Terms of service added
- [ ] Help documentation ready
- [ ] Backup strategy in place
- [ ] Monitoring set up

---

**Keep This Handy! Print it out or bookmark it! 📌**
