from flask import Flask, request, jsonify, render_template
from groq import Groq

app = Flask(__name__)

GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

# Load knowledge file safely
try:
    with open("knowledge.txt", "r", encoding="utf-8") as file:
        knowledge = file.read()
except FileNotFoundError:
    knowledge = ""
    print("knowledge.txt not found")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    if user_message.lower() in ["hi", "hello", "hey"]:
        return jsonify({"reply": "Hello! I am OptiModel. How can I help you?"})

    if knowledge and user_message.lower() not in knowledge.lower():
        return jsonify({"reply": "This question is not in my knowledge base. Try another question"})

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": f"Answer from this data:\n{knowledge}\n\nQuestion: {user_message}"
            }
        ],
    )

    bot_reply = completion.choices[0].message.content
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)