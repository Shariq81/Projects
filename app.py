from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    forecast = None
    alerts = ["Warning"]  # define alerts here
    if request.method == 'POST':
        city = request.form['city']
        api_key = '1943b6d331e781099effdef86bde4fb6'
        
        # Current Weather
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        response = requests.get(url)
        if response.status_code == 200:
            weather = response.json()
            # Process the current weather data
            current_weather = weather['main']
            wind_speed = weather['wind']['speed']
            temperature = current_weather['temp']
            severe_wind_speed = 5
            severe_temperature = 25
            if wind_speed > severe_wind_speed or temperature > severe_temperature:
                alerts.append('Severe weather alert!')
        
        # Weather Forecast
        url_forecast = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'
        response_forecast = requests.get(url_forecast)
        if response_forecast.status_code == 200:
            forecast = response_forecast.json()
            # Process the forecast data
            for day in forecast['list']:
                wind_speed = day['wind']['speed']
                temperature = day['main']['temp_max']
                if wind_speed > severe_wind_speed or temperature > severe_temperature:
                    date = day['dt_txt']  # Extract the date and time from the forecast data
                    alerts.append(f'Severe weather alert in the forecast on {date}!')

    return render_template('index.html', weather=weather, forecast=forecast, alerts=alerts)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT'))

