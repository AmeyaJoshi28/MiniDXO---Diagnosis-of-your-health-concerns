# MiniDXO | AI Diagnostic Assistant 🩺

MiniDXO is an intelligent medical diagnostic tool powered by **Gemini 2.5 Flash-Lite**. It uses a multi-agent system to interview patients, track symptom confidence in real-time, and provide a professional clinical summary.

---

## 📂 Project Structure
Based on the current architecture:
- **`/backend`**: FastAPI server, AI agents (`agents.py`), and local medical database.
- **`/frontend/frontend`**: React application, UI components, and medical dashboard styling.
- **`requirements.txt`**: Python dependencies.
- **`package.json`**: React dependencies.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- Node.js & npm
- Google Gemini API Key (from [Google AI Studio](https://aistudio.google.com/))

### 2. Backend Setup
```bash
cd backend
pip install -r ../requirements.txt
# Add your API Key in agents.py
python main.py
