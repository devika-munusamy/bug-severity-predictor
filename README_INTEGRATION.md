# Live Monitoring Integration Guide

This document explains how to integrate your applications with the **AI Bug Severity Predictor** for live monitoring.

## 1. Prerequisites

### Backend Dependencies
Ensure you have the following installed in your Python environment:
```bash
pip install flask-socketio eventlet requests
```

### Frontend Dependencies
Ensure you have the following installed in your React project:
```bash
npm install socket.io-client
```

## 2. Integration Point (Receiver)

The application now exposes a high-performance receiver endpoint:
- **URL**: `http://127.0.0.1:5000/api/v1/receive`
- **Method**: `POST`
- **Payload**:
```json
{
  "error_message": "Description of the error",
  "user_count": 5,
  "app_source": "Your-App-Name"
}
```

## 3. Real-time Monitoring Workflow

1.  **Other Applications** push live error events to the `/api/v1/receive` endpoint.
2.  **The Monitoring Server** processes the event (AI Severity Prediction + Root Cause Analysis).
3.  **The Server broadcasts** the result instantly via WebSockets (`new_bug` event).
4.  **The Dashboard** receives the event and updates the UI without a page refresh.

## 4. Example Client Integration (Python)

You can find a simulation script at `integrations/live_data_sender.py`. Here is a snippet you can use in your app:

```python
import requests

def report_error(msg, users):
    url = "http://127.0.0.1:5000/api/v1/receive"
    payload = {
        "error_message": msg,
        "user_count": users,
        "app_source": "Order-Service"
    }
    requests.post(url, json=payload)
```

## 5. Running the Simulation

To see live monitoring in action:
1. Start the API: `python api/app.py`
2. Start the Frontend: `npm start`
3. Run the sender script: `python integrations/live_data_sender.py`

New bugs will appear on your dashboard instantly!
