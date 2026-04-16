from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "your_openweathermap_api_key_here"  # i am not sharing my API key, you can get your own from openweathermap.org and replace the string above with your key


@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None

    if request.method == "POST":
        city = request.form.get("city", "").strip()

        city_clean = city.lower().strip()
        city_formatted = city_clean.title()

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_formatted}&appid={API_KEY}&units=metric"

        try:
            response = requests.get(url, timeout=5)
            data = response.json()

            print(data)

            if str(data.get("cod")) == "200":
                weather_data = {
                    "city": data.get("name", city_formatted),
                    "temp": round(data["main"]["temp"]),
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"].title()
                }
            else:
                weather_data = {
                    "error": data.get("message", "Something went wrong")
                }

        except requests.exceptions.RequestException:
            weather_data = {
                "error": "Network error, try again"
            }

    return render_template("index.html", weather=weather_data)


if __name__ == "__main__":
    app.run(debug=True)