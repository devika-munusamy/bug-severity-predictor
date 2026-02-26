# 🧠 AI Bug Intelligence Dashboard

An end-to-end AI-powered web application that predicts the severity of frontend production bugs, identifies root causes, offers fix suggestions, and detects anomalies in error rates.

This project demonstrates:
- Machine Learning model training with feature engineering
- Model serialization and inference via Flask API
- Rule-based Root Cause Analysis and Fix Suggestion Engine
- Anomaly Detection Engine monitoring error frequency
- SQLite for prediction history storage
- Modern React frontend with analytics dashboard
- Full-stack AI application architecture

---

## 🚀 Features

- **Severity Prediction**: Predicts bug severity (Low / Medium / High) with confidence and impact scores.
- **Root Cause & Fix Suggestion**: Automatically identifies potential root causes and provides actionable fix suggestions.
- **Anomaly Detection**: Monitors incoming error rates to alert on unusual spikes or widespread outages.
- **History Tracking**: Stores past predictions in a SQLite database for auditing and insights.
- **AI Analytics Dashboard**: Visualizes prediction history, severity distribution, and anomaly status with clean charting (Recharts).
- **REST API**: Cleanly separated Flask blueprints for model inference, history, and anomalies.

---

## 🏗️ Architecture

1. **React Frontend (Port 3000)**: Displays an intelligent dashboard, history table, severity pie charts, and anomaly status indicators.
2. **Flask API (Backend - Port 5000)**: Serves multiple endpoints (`/predict`, `/history`, `/anomaly-status`), manages the SQLite database, and orchestrates engines.
3. **AI Engines**:
   - Machine Learning Model (Scikit-learn) for severity.
   - Root Cause Engine for pattern matching.
   - Anomaly Detector for tracking error spikes.

---

## 📂 Project Structure

```
bug-severity-predictor/
│
├── data/                  # Datasets
├── model/                 # Model training scripts and saved models (.pkl)
├── api/
│   ├── app.py             # Flask application entry point
│   ├── db/                # SQLite database management
│   ├── routes/            # API endpoints (predict, history, anomaly)
│   └── services/          # Business logic (ML, root cause, anomaly detector)
│
├── frontend/              # React application
│   ├── public/
│   └── src/
│       ├── components/    # Reusable UI elements and charts
│       ├── pages/         # Dashboard and views
│       └── App.js
```

---

## 🛠️ Tech Stack

### Backend
- Python, Flask, Flask-CORS
- Scikit-learn, Pandas, NumPy, Joblib
- SQLite (built-in)

### Frontend
- React (React Router)
- CSS (Custom Variables & Modern UI)
- Recharts (Data Visualization)

---

## 📊 How It Works

1. Error messages and affected user counts are sent from the frontend.
2. The **ML Model** predicts the bug severity, confidence, and calculates an impact score.
3. The **Root Cause Engine** analyzes the error text to classify the category, root cause, and auto-suggests a fix.
4. The **Anomaly Detector** tracks the frequency of incoming errors to detect potential system outages.
5. Data is securely logged to the local SQLite database.
6. The frontend pulls live analytics to render an insightful, dynamic dashboard.

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone <your-repo-url>
cd bug-severity-predictor
```

### 2️⃣ Backend Setup

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3️⃣ Train the Model Engine

```bash
cd model
python train.py
cd ..
```

*This generates the `model.pkl` and `vectorizer.pkl` files used by the API.*

### 4️⃣ Start Backend Server

```bash
cd api
python app.py
```

Backend runs at: `http://127.0.0.1:5000`

### 5️⃣ Frontend Setup

Open a new terminal:

```bash
cd frontend
npm install
npm start
```

Frontend runs at: `http://localhost:3000`

---

## 🔌 Core API Endpoints

### POST `/predict`
Predicts severity, runs root cause analysis, checks anomalies, and saves tracking history.
**Request**: `{"error_message": "Network error", "user_count": 100}`
**Response**: Detailed JSON with prediction, root cause, suggested fix, and metrics.

### GET `/history`
Fetches a list of all past errors logged in the database.

### GET `/anomaly-status`
Checks if there's currently an anomaly based on recent error volume.

---

## 📈 Future Improvements

- Replace classical ML with LLM-based classifier (e.g., OpenAI or local Llama model)
- Implement user authentication & authorization
- Add Docker setup for containerized deployments
- Add live WebSocket streams for real-time anomaly alerts
- Expand dataset size and train on a wider variety of logs

---

## 🎯 Why This Project Is Valuable

This project demonstrates:
- Building an intelligence layer over traditional logging.
- Practical Machine Learning & heuristics implementation.
- API Design with Flask blueprints and service separation.
- Frontend-backend integration with interactive charting.
- Real-world SaaS-inspired use case.

---

## 👩‍💻 Author

Devika Munusamy
Software Engineer | Frontend & Full-Stack Developer
Exploring Applied AI Systems