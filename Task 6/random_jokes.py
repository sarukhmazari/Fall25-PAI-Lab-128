from flask import Flask, jsonify, send_file
import requests
import os

app = Flask(__name__)

# Serve HTML directly
@app.route('/')
def home():
    return send_file(os.path.join(os.path.dirname(__file__), 'index.html'))

# Joke API
@app.route('/joke')
def get_joke():
    try:
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        response.raise_for_status()
        joke_data = response.json()
        joke = {
            "setup": joke_data.get('setup', 'No setup available'),
            "punchline": joke_data.get('punchline', 'No punchline available')
        }
    except requests.RequestException as e:
        joke = {"error": f"Could not fetch a joke: {str(e)}"}
    except Exception as e:
        joke = {"error": f"Unexpected error: {str(e)}"}

    return jsonify(joke)

if __name__ == '__main__':
    app.run(debug=True)