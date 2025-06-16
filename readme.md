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
