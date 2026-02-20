# 🧠 AI Bug Severity Predictor

An end-to-end AI-powered web application that predicts the severity of frontend production bugs based on error messages.

This project demonstrates:
- Machine Learning model training
- Model serialization
- Flask API for inference
- React frontend integration
- Full-stack AI application architecture

---

## 🚀 Features

- Predicts bug severity (Low / Medium / High)
- Returns confidence score
- REST API for model inference
- Clean React UI
- Cross-origin communication handled via CORS
- Structured full-stack architecture

---

## 🏗️ Architecture

React (Frontend - Port 3000)
⬇
Flask API (Backend - Port 5000)
⬇
Trained ML Model (Scikit-learn)

---

## 📂 Project Structure

bug-severity-predictor/
│
├── data/
│   └── bugs.csv
│
├── model/
│   ├── train.py
│   └── model.pkl
│
├── api/
│   └── app.py
│
├── frontend/
│   └── React application
│
├── venv/
├── requirements.txt
└── README.md

---

## 🛠️ Tech Stack

### Backend
- Python
- Flask
- Flask-CORS
- Scikit-learn
- Pandas
- NumPy
- Joblib

### Frontend
- React
- Fetch API
- CSS

---

## 📊 How It Works

1. Error messages are converted into numerical vectors using TF-IDF.
2. A Logistic Regression classifier predicts the severity.
3. The trained model is saved using joblib.
4. Flask loads the model and exposes a `/predict` endpoint.
5. React sends user input to the backend.
6. Backend returns predicted severity + confidence score.

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

git clone <your-repo-url>
cd bug-severity-predictor

---

### 2️⃣ Backend Setup

Create virtual environment:

python3 -m venv venv
source venv/bin/activate

Install dependencies:

pip install flask flask-cors pandas scikit-learn numpy joblib

(Optional) Save dependencies:

pip freeze > requirements.txt

---
(future use)

pip install -r requirements.txt

### 3️⃣ Train the Model

cd model
python train.py

This generates:

model.pkl

---

### 4️⃣ Start Backend Server

cd ../api
python app.py

Backend runs at:

http://127.0.0.1:5000

---

### 5️⃣ Frontend Setup

Open new terminal:

cd frontend
npm install
npm start

Frontend runs at:

http://localhost:3000

---

## 🔌 API Endpoint

### POST `/predict`

Request:

{
  "error_message": "Payment gateway failed for 100 users"
}

Response:

{
  "severity": "High",
  "confidence": 0.92
}

---

## 📈 Future Improvements

- Add user_count as additional feature
- Improve dataset size and quality
- Store prediction history in database
- Add severity analytics dashboard
- Add authentication
- Dockerize application
- Deploy to cloud (Render / AWS / Railway)
- Replace classical ML with LLM-based classifier

---

## 🎯 Why This Project Is Valuable

This project demonstrates:

- Practical Machine Learning implementation
- Model deployment as API
- Frontend-backend integration
- End-to-end AI product development
- Real-world SaaS-inspired use case

---

## 👩‍💻 Author

Devika Munusamy
Software Engineer | Frontend & Full-Stack Developer
Exploring Applied AI Systems