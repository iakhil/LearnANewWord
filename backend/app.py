from flask import Flask, request, jsonify
import os
from openai import OpenAI
from dotenv import load_dotenv
from flask_cors import CORS

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

CORS(app)

# Initialize OpenAI client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

@app.route("/api/rate-meaning", methods=["POST"])
def rate_meaning():
    try:
        # Extract data from the request
        data = request.json
        user_meaning = data.get("user_meaning")
        actual_meaning = data.get("actual_meaning")

        # Validate inputs
        if not user_meaning or not actual_meaning:
            return jsonify({"error": "Both user_meaning and actual_meaning are required."}), 400

        # OpenAI API call
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an assistant that evaluates the accuracy of user-provided meanings. Provide a rating from 1 to 5 based on how accurate the user's meaning is compared to the actual meaning. Only return the number as a response."
                },
                {
                    "role": "user",
                    "content": f"Rate the accuracy of the following user meaning:\nUser meaning: \"{user_meaning}\"\nActual meaning: \"{actual_meaning}\""
                }
            ],
            model="gpt-4",
        )

        # Extract and return the response
        rating = chat_completion.choices[0].message.content
        # rating = chat_completion["choices"][0]["message"]["content"].strip()
        return jsonify({"rating": rating})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/rate-sentence", methods=["POST"])
def rate_sentence():
    try:
        data = request.json
        user_sentence = data.get("user_sentence")
        word = data.get("word")

        if not user_sentence or not word:
            return jsonify({"error": "Both user_sentence and word are required."}), 400

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an assistant that evaluates user-provided sentences. Rate the sentence from 1 to 5 based on how effectively the sentence uses the provided word. Only return the number as a response."
                },
                {
                    "role": "user",
                    "content": f"Rate the effectiveness of the following sentence:\nSentence: \"{user_sentence}\"\nWord: \"{word}\""
                }
            ],
            model="gpt-4",
        )

        rating = chat_completion.choices[0].message.content
        return jsonify({"rating": rating})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
