# SETUP GUIDE - Smart Photo Share

## Day 1 Setup Instructions

### Prerequisites Installation

#### 1. Install Python 3.9+ (if not installed)
```bash
# Check Python version
python --version  # or python3 --version

# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# macOS (using Homebrew)
brew install python@3.9

# Windows
# Download from https://www.python.org/downloads/
```

#### 2. Install Node.js 16+ (if not installed)
```bash
# Check Node version
node --version

# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# macOS (using Homebrew)
brew install node

# Windows
# Download from https://nodejs.org/
```

#### 3. Install System Dependencies for face_recognition
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y build-essential cmake
sudo apt-get install -y libopenblas-dev liblapack-dev
sudo apt-get install -y libx11-dev libgtk-3-dev

# macOS
brew install cmake

# Windows
# Install Visual C++ Build Tools from:
# https://visualstudio.microsoft.com/downloads/
```

---

## Backend Setup (Person 1 Task)

### Step 1: Navigate to backend directory
```bash
cd photo-share-app/backend
```

### Step 2: Create virtual environment
```bash
python3 -m venv venv

# Activate it
# Linux/Mac:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### Step 3: Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Note:** Installing `face_recognition` may take 5-10 minutes as it compiles dlib.

### Step 4: Initialize database
```bash
python init_db.py
```

You should see: "✅ Database setup complete!"

### Step 5: Start the backend server
```bash
python main.py
```

The server will start on `http://localhost:8000`

You should see:
```
✅ Server started successfully!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 6: Test the API
Open a new terminal and test:
```bash
curl http://localhost:8000/
```

You should see: `{"message":"Smart Photo Share API","status":"running"}`

---

## Frontend Setup (Person 2 Task)

### Step 1: Navigate to frontend directory
```bash
cd photo-share-app/frontend
```

### Step 2: Install dependencies
```bash
npm install
```

This will install React and all required packages.

### Step 3: Start the development server
```bash
npm start
```

The app will open in your browser at `http://localhost:3000`

You should see the login page!

---

## Testing the Complete Flow

### Test 1: User Registration and Face Enrollment

1. **Register a new user:**
   - Go to `http://localhost:3000/register`
   - Fill in details (name, email, password)
   - Click "Register"
   - You'll be redirected to face enrollment

2. **Enroll face:**
   - Upload 3-5 clear photos of yourself
   - Photos should have good lighting and your face clearly visible
   - Click "Enroll Face"
   - Wait for processing (takes ~10-30 seconds)
   - You'll be redirected to dashboard

### Test 2: Upload Photos

1. **Go to "Upload Photos"**
2. **Select 5-10 test photos** containing people
3. **Optional:** Add event name (e.g., "Test Event")
4. **Click "Upload & Process"**
5. Wait for upload and processing to complete

### Test 3: View Your Photos

1. **Go to "My Photos"**
2. You should see all photos where you appear
3. Click on any photo to view full size
4. Test the download functionality

### Test 4: Multi-User Testing

1. **Register 2-3 more users** (use different browsers or incognito mode)
2. **Each user enrolls their face** with their own photos
3. **Upload group photos** (photos with multiple enrolled users)
4. **Check each user's "My Photos"** - they should only see photos they appear in

---

## Common Issues and Solutions

### Issue 1: face_recognition installation fails
**Solution:**
```bash
# Install cmake first
pip install cmake

# Then install face_recognition
pip install face-recognition
```

### Issue 2: "No module named 'face_recognition'"
**Solution:**
Make sure virtual environment is activated:
```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Issue 3: Port 8000 or 3000 already in use
**Solution:**
```bash
# Find and kill process using the port
# Linux/Mac:
lsof -ti:8000 | xargs kill -9
lsof -ti:3000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Issue 4: CORS errors in browser
**Solution:**
Make sure backend is running and `CORS` is properly configured in `main.py` (already done).

### Issue 5: Face detection not working
**Solution:**
- Use well-lit photos
- Ensure face is clearly visible
- Face should be front-facing (not profile)
- Minimum 100x100 pixels face size

---

## Development Tips

### Backend Development (Person 1)
- **API Docs:** Visit `http://localhost:8000/docs` for interactive API documentation
- **Database:** SQLite file is created at `backend/photo_share.db`
- **Logs:** Check terminal for error messages
- **Test API:** Use Postman or curl for testing endpoints

### Frontend Development (Person 2)
- **Hot Reload:** Changes auto-refresh in browser
- **React DevTools:** Install browser extension for debugging
- **Console:** Check browser console for errors (F12)
- **Network Tab:** Monitor API calls in browser DevTools

### Collaboration Tips
1. **Person 1** focuses on backend API endpoints
2. **Person 2** focuses on frontend UI/UX
3. **Test together** after major features
4. Use Git for version control (commit often!)

---

## Next Steps After Setup

### Week 1 Goals:
- ✅ Complete setup (Day 1)
- Add more API endpoints (Person 1)
- Improve UI design (Person 2)
- Add error handling
- Test with real photos

### Week 2 Goals:
- Add batch processing for large uploads
- Improve face matching accuracy
- Add event management features
- Create shareable links

### Week 3 Goals:
- Deploy to cloud (Railway/Heroku)
- User testing with real users
- Bug fixes and optimizations
- Prepare for demo

---

## Project Structure Reference

```
photo-share-app/
├── backend/
│   ├── main.py                    # FastAPI app and routes
│   ├── models.py                  # Database models
│   ├── face_recognition_service.py # Face detection logic
│   ├── requirements.txt           # Python dependencies
│   ├── init_db.py                # Database setup script
│   └── photo_share.db            # SQLite database (created on init)
│
├── frontend/
│   ├── src/
│   │   ├── App.js                # Main React component
│   │   ├── App.css               # Styling
│   │   ├── pages/                # Page components
│   │   │   ├── Login.js
│   │   │   ├── Register.js
│   │   │   ├── Dashboard.js
│   │   │   ├── EnrollFace.js
│   │   │   ├── UploadPhotos.js
│   │   │   └── MyPhotos.js
│   │   └── index.js              # React entry point
│   ├── public/
│   │   └── index.html            # HTML template
│   └── package.json              # Node dependencies
│
├── uploads/                      # Photo storage
│   ├── originals/                # Full resolution photos
│   ├── faces/                    # Face enrollment photos
│   └── thumbnails/               # Thumbnail versions
│
└── README.md                     # Project overview
```

---

## Git Setup (Recommended)

```bash
cd photo-share-app
git init
echo "venv/" >> .gitignore
echo "node_modules/" >> .gitignore
echo "*.db" >> .gitignore
echo "uploads/" >> .gitignore
echo ".env" >> .gitignore
git add .
git commit -m "Initial commit - Smart Photo Share MVP"
```

---

## Support and Resources

- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **React Docs:** https://react.dev/
- **face_recognition:** https://github.com/ageitgey/face_recognition
- **SQLAlchemy:** https://docs.sqlalchemy.org/

---

## Success Criteria for Day 1

- [ ] Backend server running on port 8000
- [ ] Frontend app running on port 3000
- [ ] Can register a new user
- [ ] Can enroll face with test photos
- [ ] Can upload and process test photos
- [ ] Can view photos in gallery
- [ ] No critical errors in console/terminal

**If all checkboxes are checked - YOU'RE READY TO BUILD! 🚀**
