# PromptWars AI Project Mentor
Hackathon MVP for: AI Project Idea Generator & Mentor for Final-Year Projects.

Stack: Streamlit frontend + FastAPI backend + optional Gemini API + Docker + Render.

Core features:
1. Smart Idea Generator
2. Tech Stack Selector
3. Interactive AI Mentor

Run backend:
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

Run frontend in another terminal:
cd frontend
pip install -r requirements.txt
streamlit run app.py

Without GEMINI_API_KEY the app runs in demo mode. Put a real key in an environment variable; never commit it.
