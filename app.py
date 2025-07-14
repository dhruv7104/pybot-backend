from flask import Flask, request, jsonify
from flask_cors import CORS
from fuzzywuzzy import fuzz

app = Flask(__name__)
CORS(app)  # Allow React frontend to access Flask API

# Sample fuzzy-response chatbot logic
def get_response(user_input):
    user_input = user_input.lower()

    known_qna = {
        "who is virat kohli": "Virat Kohli is an Indian cricketer, widely regarded as one of the best batsmen in the world.",
        "hello": "Hello there! How can I assist you today?",
        "hi": "Hi! I'm PyBot. Ask me anything.",
        "what is photosynthesis": "Photosynthesis is the process by which green plants convert sunlight into chemical energy.",
        "how are you": "I'm just a bunch of code, but thanks for asking! 😊",
        "bye": "Goodbye! Have a great day!"
    }

    for question, answer in known_qna.items():
        if fuzz.ratio(user_input, question) > 80:
            return answer

    return "I'm not sure I understand. Try rephrasing your question or ask something else."

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    reply = get_response(user_message)
    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True)
