🧠 MindEase — Mental Health Assistant

MindEase is a secure, AI-powered mental health chat application built with Streamlit.
It provides users with a private space to talk, reflect, and receive empathetic support through conversational AI.

⚠️ MindEase is not a replacement for professional mental health care.
If you feel unsafe or in crisis, please contact your local emergency services or a crisis hotline.

✨ What This App Does

🔐 User Authentication

Sign up and log in securely

Passwords are hashed (SHA-256)

💬 AI Chat Support

Empathetic, conversational mental health assistant (“Sage”)

Context-aware responses within each conversation

🧵 Conversation History

Each user can have multiple conversations

Messages are stored and retrieved from a database

🚨 Crisis Awareness

Encourages professional help when appropriate

Displays crisis resources in the UI

☁️ Streamlit Cloud Ready

SQLite + SQLAlchemy configured for cloud deployment

Thread-safe database setup

🤖 AI Used

MindEase uses Groq’s LLM API for fast and reliable AI responses.

Model:

llama-3.1-8b-instant

Why Groq?

Extremely fast inference

Free / low-cost tier available

No OpenAI quota or billing issues

Stable Python SDK

The AI is prompted to:

Respond empathetically

Avoid repetition

Ask thoughtful follow-up questions

Never provide medical diagnoses

🛠 Tech Stack

Frontend: Streamlit

Backend: Python

Database: SQLite + SQLAlchemy

AI Provider: Groq

Auth: Custom email/password authentication

Hosting: Streamlit Cloud compatible

🚀 How to Run the App
1️⃣ Clone the Repository
git clone https://github.com/your-username/mindease.git
cd mindease

2️⃣ Create & Activate Virtual Environment
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt


requirements.txt

streamlit==1.38.0
sqlalchemy==2.0.32
groq==0.9.0
pyyaml==6.0.2

4️⃣ Set Environment Variables

Create a .env file or set manually:

export GROQ_API_KEY="your_groq_api_key"


Windows:

setx GROQ_API_KEY "your_groq_api_key"

5️⃣ Run the App
streamlit run app.py


Open your browser at:

http://localhost:8501

📂 Project Structure
mindease/
│
├── app.py
├── requirements.txt
│
├── src/
│   ├── components/
│   │   ├── AuthForm.py
│   │   ├── ChatInterface.py
│   │   └── CrisisResourcesBanner.py
│   │
│   ├── database/
│   │   ├── models.py
│   │   └── __init__.py
│   │
│   └── utils/
│       ├── auth.py
│       └── openai_client.py

🧩 Disclaimer

MindEase is designed for emotional support and reflection only.
It does not provide medical, psychological, or psychiatric advice.

If you are in immediate danger or distress, please contact:

🇺🇸 988 — Suicide & Crisis Lifeline

🌍 Local emergency services

❤️ Final Note

MindEase was built to make people feel heard, supported, and less alone.
Thank you for taking the time to explore it.

If you’d like help adding:

Streaming responses

Multi-model AI fallback

Journaling mode

Mood tracking
