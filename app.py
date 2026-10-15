from flask import Flask, request, render_template, jsonify
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


app = Flask(__name__)

# Route for the main page
@app.route("/")
def index():
    return render_template("index.html")

# Route to process code input
@app.route("/analyze", methods=["POST"])
def analyze_code():
    data = request.json
    code_snippet = data.get("code")

    if not code_snippet or not code_snippet.strip():
        return jsonify({"error": "Code input cannot be empty"}), 400

    try:
        # Use OpenAI API to analyze the code
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that explains code"},
                {"role": "user", "content": f"Explain the following code:\n{code_snippet}"}
            ],
            max_tokens=1500
        )
        explanation = response.choices[0].message["content"].strip()
        return jsonify({"explanation": explanation})
    except Exception as e:
        return jsonify({"error": f"Error processing request: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
