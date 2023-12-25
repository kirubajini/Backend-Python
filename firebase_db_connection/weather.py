from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace with your OpenWeatherMap API key
OPENWEATHERMAP_API_KEY = 'aca0a8a301d610ce3d6188ba4a880140'


@app.route('/weather', methods=['POST'])
def get_weather():
    data = request.get_json()
    print("data: ", data)
    city_name = data.get('city', '')

    if not city_name:
        return jsonify({"error": "City not specified"}), 400

    current_weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={OPENWEATHERMAP_API_KEY}&units=metric'
    forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={OPENWEATHERMAP_API_KEY}&units=metric'

    try:
        current_response = requests.get(current_weather_url)
        forecast_response = requests.get(forecast_url)

        current_data = current_response.json()
        forecast_data = forecast_response.json()

        if current_response.status_code == 200 and forecast_response.status_code == 200:
            current_weather_info = {
                "temperature": current_data['main']['temp'],
                "description": current_data['weather'][0]['description'],
                "humidity": current_data['main']['humidity'],
                "windspeed": current_data['wind']['speed']
            }

            # Extract precipitation volume in mm from the forecast data
            rain_volume_mm = forecast_data['list'][0]['rain']['3h'] if 'rain' in forecast_data['list'][0] else 0

            # Define a rule to calculate precipitation as a percentage
            # You may need to adjust this rule based on your specific criteria
            max_rain_mm = 10  # You consider this amount as 100% precipitation
            precipitation_percentage = int((rain_volume_mm / max_rain_mm) * 100)

            current_weather_info["precipitation_percentage"] = str(precipitation_percentage) + "%"

            print("current_weather_info: ", current_weather_info)
            return jsonify(current_weather_info)

        error_message = current_data.get('message', 'An error occurred.')
        return jsonify({"error": error_message}), current_response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "An error occurred while making the request"}), 500


if __name__ == "__main__":
    app.run(debug=True)
