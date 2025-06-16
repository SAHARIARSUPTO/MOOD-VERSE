# MoodVerse - AI Mood Detection Platform

MoodVerse is a full-stack web application that detects user moods using AI and responds with memes, music, or suggestions based on the mood.

## Tech Stack

- Frontend: Next.js, TailwindCSS, Framer Motion
- Backend: Python 3.10 (Custom server without FastAPI)
- Mood Detection: OpenCV, DeepFace or FER+
- Database: MongoDB
- Node.js Server: Handles additional routes or services if needed

## How to Run Locally

### Requirements

- Python 3.10
- Node.js (v16 or later)
- MongoDB (local or cloud)
- Git

## Project Structure

/moodverse
│
├── client/               # Next.js frontend
├── server/               # Python backend (custom script)
├── node-server/          # Optional Node.js server
└── README.md

## 1. Backend Setup (Python)

```bash
cd server

# Create a virtual environment
python -m venv venv
source venv/bin/activate      # For Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set PYTHONPATH for local module imports

# Linux/macOS
export PYTHONPATH=$(pwd)

# Windows CMD
set PYTHONPATH=%cd%

# Start your custom Python backend script
python main.py
2. Node.js Server Setup (Optional)
bash
Copy
Edit
cd node-server
npm install
npm run dev
3. Frontend Setup (Next.js)
bash
Copy
Edit
cd client
npm install

# Copy and configure environment variables
cp .env.example .env.local
# Edit .env.local with your backend URL if needed

npm run dev
Environment Variables
.env.local (Frontend)
ini
Copy
Edit
NEXT_PUBLIC_API_URL=http://localhost:8000
Python Backend
Set manually or use dotenv in your script:

bash
Copy
Edit
MONGO_URI=mongodb://localhost:27017/moodverse
Test the App
Run MongoDB locally or connect to MongoDB Atlas.

Start the backend (python main.py or whatever your script is).

Start the frontend (npm run dev in client/).

Visit http://localhost:3000 in your browser.

Common Issues
Make sure Python 3.10 is installed and selected.

MongoDB must be running or the backend will fail to connect.

Set PYTHONPATH before running Python scripts to avoid import errors.

License
MIT License


---

Let me know if your Python backend file is not `main.py`, and I’ll tweak the instructions accordingly. You can now copy this directly into your `README.md` file.
