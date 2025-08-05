from flask import Flask, render_template, request
import requests
import pickle
import numpy as np
from datetime import datetime, timedelta

app = Flask(__name__)

# Load trained ML model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Ajmer coordinates (fixed)
AJMER_LAT = 26.4499
AJMER_LON = 74.6399
API_KEY = "50eac6a47d10831cbe3fb32d5abae06f"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict_today", methods=["POST"])
def predict_today():
    max_temp = float(request.form["max_temp"])
    min_temp = float(request.form["min_temp"])
    humidity = float(request.form["humidity"])

    # Make predictions
    features = np.array([[max_temp, min_temp, humidity]])

    rain_chance = model['clf_rain_chance'].predict(features)[0]
    rain_chance_prob = model['clf_rain_chance'].predict_proba(features)[0][1] * 100
    rain_timing_encoded = model['clf_timing'].predict(features)[0]
    rain_type_encoded = model['clf_type'].predict(features)[0]
    rain_amount = model['reg_rain_amt'].predict(features)[0]

    rain_timing = model['le_timing'].inverse_transform([rain_timing_encoded])[0]
    rain_type = model['le_type'].inverse_transform([rain_type_encoded])[0]

    today_date = datetime.now().strftime('%Y-%m-%d')

    prediction = {
        "date": today_date,
        "max_temp": max_temp,
        "min_temp": min_temp,
        "humidity": humidity,
        "rain_probability": round(rain_chance_prob, 1),
        "rain_timing": rain_timing,
        "rain_type": rain_type,
        "rain_amount": round(max(0, rain_amount), 1)
    }

    return render_template("prediction.html", prediction=prediction, is_today=True)

@app.route("/forecast_5days", methods=["POST"])
def forecast_5days():
    max_temp = float(request.form["max_temp"])
    min_temp = float(request.form["min_temp"])
    humidity = float(request.form["humidity"])

    forecasts = []

    for i in range(5):
        date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')

        temp_variation = np.random.uniform(-2, 2)
        humidity_variation = np.random.uniform(-5, 5)

        day_max_temp = max_temp + temp_variation
        day_min_temp = min_temp + temp_variation
        day_humidity = max(0, min(100, humidity + humidity_variation))

        features = np.array([[day_max_temp, day_min_temp, day_humidity]])

        rain_chance = model['clf_rain_chance'].predict(features)[0]
        rain_chance_prob = model['clf_rain_chance'].predict_proba(features)[0][1] * 100
        rain_timing_encoded = model['clf_timing'].predict(features)[0]
        rain_type_encoded = model['clf_type'].predict(features)[0]
        rain_amount = model['reg_rain_amt'].predict(features)[0]

        rain_timing = model['le_timing'].inverse_transform([rain_timing_encoded])[0]
        rain_type = model['le_type'].inverse_transform([rain_type_encoded])[0]

        forecasts.append({
            "date": date,
            "max_temp": round(day_max_temp, 1),
            "min_temp": round(day_min_temp, 1),
            "humidity": round(day_humidity, 1),
            "rain_probability": round(rain_chance_prob, 1),
            "rain_timing": rain_timing,
            "rain_type": rain_type,
            "rain_amount": round(max(0, rain_amount), 1)
        })

    return render_template("prediction.html", forecasts=forecasts, is_today=False)

@app.route("/forecast_5days_auto")
def forecast_5days_auto():
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={AJMER_LAT}&lon={AJMER_LON}&units=metric&appid={API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        return f"API Error: {response.status_code}"

    data = response.json()

    if 'list' not in data:
        return f"API Response Error: {data}"

    daily_data = {}

    for item in data['list']:
        date_str = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')

        if date_str not in daily_data:
            daily_data[date_str] = {
                'temps': [],
                'humidities': [],
                'date': date_str
            }

        daily_data[date_str]['temps'].append(item['main']['temp'])
        daily_data[date_str]['humidities'].append(item['main']['humidity'])

    forecasts = []

    for date_str in sorted(daily_data.keys())[:5]:
        day_data = daily_data[date_str]

        max_temp = max(day_data['temps'])
        min_temp = min(day_data['temps'])

        # ✅ CHANGED: Use maximum humidity instead of average
        avg_humidity = max(day_data['humidities'])

        features = np.array([[max_temp, min_temp, avg_humidity]])

        rain_chance = model['clf_rain_chance'].predict(features)[0]
        rain_chance_prob = model['clf_rain_chance'].predict_proba(features)[0][1] * 100
        rain_timing_encoded = model['clf_timing'].predict(features)[0]
        rain_type_encoded = model['clf_type'].predict(features)[0]
        rain_amount = model['reg_rain_amt'].predict(features)[0]

        rain_timing = model['le_timing'].inverse_transform([rain_timing_encoded])[0]
        rain_type = model['le_type'].inverse_transform([rain_type_encoded])[0]

        forecasts.append({
            "date": date_str,
            "max_temp": round(max_temp, 1),
            "min_temp": round(min_temp, 1),
            "humidity": round(avg_humidity, 1),
            "rain_probability": round(rain_chance_prob, 1),
            "rain_timing": rain_timing,
            "rain_type": rain_type,
            "rain_amount": round(max(0, rain_amount), 1)
        })

    return render_template("prediction.html", forecasts=forecasts, is_today=False)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
