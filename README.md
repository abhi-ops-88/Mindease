# Mindease
This is an application talks about mental health and guide and coaches the users
# 🧠 MindEase — AI Mental Health Assistant

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mindease-mvp.streamlit.app)

**Live Demo:** [https://mindease-mvp.streamlit.app](https://mindease-mvp.streamlit.app)

**MindEase** is a **production-ready AI mental health support app** built with **Streamlit + OpenAI GPT-4o-mini**.  
Provides empathetic conversations with **crisis resource awareness** and **full chat persistence**.

---

## 🌟 ✨ LIVE FEATURES

| ✅ **Secure Authentication** | SHA-256 hashed passwords + SQLite |
| ✅ **Sage AI Assistant** | GPT-4o-mini with mental health prompt |
| ✅ **Chat History** | User-specific conversations |
| ✅ **Crisis Banner** | 988 Lifeline + emergency contacts |
| ✅ **Multi-Chat** | Sidebar conversation switching |
| ✅ **Responsive UI** | Gradient design + message bubbles |

---

## 🧠 AI Technology
🤖 Model: GPT-4o-mini (OpenAI)
💬 API: Chat Completions
🎯 Purpose: Empathetic mental health support
⚡ Features: Context-aware, crisis-aware responses

---

## ⚙️ Tech Stack

Frontend: Streamlit (Python)
Database: SQLite + SQLAlchemy ORM
AI: OpenAI GPT-4o-mini API
Security: SHA-256 hashing
Deployment: Streamlit Cloud
Structure: Multi-file src/components/

---

## 🚀 Try Live Demo

**URL:** [https://mindease-mvp.streamlit.app](https://mindease-mvp.streamlit.app)

**Test Account:**
Email: test@example.com
Username: 
Password: 


---

## 🛠 Local Setup (5 Minutes)

### 1. Clone Repository
git clone <your-github-repo>
cd mindease


### 2. Install Dependencies
pip install -r requirements.txt



### 3. Add OpenAI Key
Create `.streamlit/secrets.toml`:
OPENAI_API_KEY = "sk-your-openai-key"


### 4. Run App
streamlit run app.py

**Opens:** `http://localhost:8501`

---

## ☁️ Streamlit Cloud Deployment

**Status:** ✅ **ALREADY LIVE!**


---

## 📁 Production File Structure

mindease/
├── app.py # Main entrypoint
├── requirements.txt # Dependencies
├── README.md # This file!
└── src/
├── init.py
├── components/ # React.tsx equivalent
│ ├── AuthForm.py # AuthForm.tsx
│ ├── CrisisResourcesBanner.py # CrisisResourcesBanner.tsx
│ └──
