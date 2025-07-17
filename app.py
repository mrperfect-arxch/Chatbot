from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message')
        print(f"Received message: {message}")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}]
        )

        reply = response['choices'][0]['message']['content'].strip()
        return jsonify({"reply": reply})
    except Exception as e:
        print(f"Error in /chat endpoint: {e}")
        return jsonify({"error": "Backend error"}), 500

@app.route('/generate-image', methods=['POST'])
def generate_image():
    try:
        data = request.json
        prompt = data.get('prompt')
        print(f"Received image prompt: {prompt}")

        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        image_url = response['data'][0]['url']
        return jsonify({"image_url": image_url})
    except Exception as e:
        print(f"Error in /generate-image endpoint: {e}")
        return jsonify({"error": "Backend error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
