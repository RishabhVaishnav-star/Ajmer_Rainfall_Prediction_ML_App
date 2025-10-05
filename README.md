# 🌧️ Ajmer Rainfall Prediction Web App

## 📘 Overview
This project is a **Machine Learning-based Flask web application** that predicts the probability of rainfall in **Ajmer (Rajasthan)** using real-time weather forecast data fetched from the **OpenWeatherMap One Call API (2.5)**.

The app analyzes **7-day forecast data**, including:
- 🌡️ Maximum Temperature  
- 🌡️ Minimum Temperature  
- 💧 Humidity  

Based on these values, the trained ML model (`model.pkl`) predicts whether **rainfall is likely** for each of the next 7 days.

---

## 🌐 Live Demo
🔗 **[Ajmer Rainfall Prediction App on Render](https://ajmer-rainfall-prediction.onrender.com/)**  
*(Note: May take 30–60 seconds to load initially due to Render’s free hosting plan.)*

---

## 🧠 Features
✅ Fetches **7-day forecast automatically** using OpenWeatherMap API  
✅ Predicts **rainfall probability** using an ML model  
✅ Displays results in a clean, responsive web interface  
✅ Built with **Flask**, **scikit-learn**, and **pandas**  
✅ Deployed on **Render** and available publicly  

---

## 🧩 Tech Stack

| Category | Technologies Used |
|-----------|-------------------|
| **Backend** | Flask (Python) |
| **Machine Learning** | scikit-learn |
| **Data Processing** | pandas, NumPy |
| **API Integration** | OpenWeatherMap One Call API (2.5) |
| **Deployment** | Render |
| **Frontend** | HTML, CSS |

---

## 🗂️ Project Structure
rainfall-prediction/
│
├── app.py # Flask backend application
├── model.pkl # Trained ML model (serialized)
├── templates/
│ └── index.html # Frontend HTML template
├── static/
│ └── style.css # Styling (optional)
├── requirements.txt # Python dependencies
├── Procfile # Render process configuration
└── README.md # Project documentation


---
## ⚙️ Local Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/rainfall-prediction.git
cd rainfall-prediction
2️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt
3️⃣ Run the Flask app
bash
Copy code
python app.py
4️⃣ Open in browser
cpp
Copy code
http://127.0.0.1:5000/
🌦️ Weather Data Source
API: OpenWeatherMap One Call API (2.5)

Used to fetch:
Daily Maximum Temperature
Daily Minimum Temperature
Daily Maximum Humidity

The coordinates for Ajmer (26.45°N, 74.64°E) are fixed within the app — no user input required.

🧮 Model Description
The ML model (model.pkl) is trained using historical weather data to classify whether it will rain or not based on:

Max Temperature
Min Temperature
Humidity

The model outputs:

🌧️ Rain Likely
☀️ No Rain

Deployment:
Using render.com

