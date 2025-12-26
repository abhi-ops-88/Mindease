# 🧠 MindEase — Mental Health Chat Assistant  

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mindease-mvp.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit Cloud](https://img.shields.io/badge/Streamlit-Cloud-brightgreen.svg)](https://mindease-mvp.streamlit.app/)
[![Live Demo](https://img.shields.io/badge/Live-Demo-%23FF6B6B.svg)](https://mindease-mvp.streamlit.app/)

**MindEase** is a secure, AI-powered mental health chat application built with **Streamlit**.  
It offers a private, empathetic space where users can talk, reflect, and receive support from an AI designed to listen and understand.  

**[Try it live now →](https://mindease-mvp.streamlit.app/)**  

⚠️ *MindEase is not a substitute for professional mental health care.*  
If you are in crisis, please contact your local emergency services or a crisis hotline.  

---

## ✨ Features  

### 🔐 Authentication  
- Secure email/password login  
- Passwords hashed with **SHA-256**

### 💬 AI Chat Support  
- Empathetic conversational AI (*Sage*)  
- Context-aware and emotionally intelligent responses  

### 🧵 Conversation History  
- Multiple sessions per user  
- Messages stored and retrieved from a database  

### 🚨 Crisis Awareness  
- Prompts users to seek professional help when needed  
- Displays crisis hotlines and resources  

### ☁️ Cloud Ready  
- **Live on Streamlit Cloud**: [mindease-mvp.streamlit.app](https://mindease-mvp.streamlit.app/)  
- Built with **SQLite + SQLAlchemy** and thread-safe database setup  

---

## 🤖 AI Model  

**Provider:** [Groq LLM API](https://groq.com)  
**Model:** `llama-3.1-8b-instant`  

**Why Groq?**  
- Ultra-fast response times  
- Free / low-cost tier  
- No OpenAI billing or quota issues  
- Stable Python SDK  

**AI Behavior:**  
- Responds empathetically  
- Avoids repetition  
- Asks thoughtful follow-up questions  
- No medical advice or diagnosis  

---

## 🛠 Tech Stack  

| Component | Technology |
|------------|-------------|
| Frontend | Streamlit |
| Backend | Python |
| Database | SQLite + SQLAlchemy |
| AI Provider | Groq |
| Authentication | Custom email/password |
| Hosting | Streamlit Cloud |

---

## 🚀 Getting Started  

### 🌐 **Live Demo**  
**[https://mindease-mvp.streamlit.app/](https://mindease-mvp.streamlit.app/)**  
*No setup required — try it instantly!*

### 🖥️ **Local Development**  

#### 1️⃣ Clone Repository  
