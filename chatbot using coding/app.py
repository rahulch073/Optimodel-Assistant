from flask import Flask, request, jsonify, render_template
from groq import Groq

app = Flask(__name__)

GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

# Load knowledge file
with open("knowledge.txt", "r", encoding="utf-8") as file:
    knowledge = file.read()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    if user_message.lower() in ["hi", "hello", "hey"]:
        return jsonify({"reply": "Hello!I am OptiModel :AI MODEL TRAINING OPTIMIZATION ASSISTANT! How can i help you?"})

    if user_message.lower() not in knowledge.lower():
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