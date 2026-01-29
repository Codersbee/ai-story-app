import os
from flask import Flask, request, jsonify
from groq import Groq

from dotenv import load_dotenv



load_dotenv()   # 👈 THIS LINE IS CRITICAL

app = Flask(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
print(os.getenv("GROQ_API_KEY"))


@app.route("/create-story", methods=["POST"])
def create_story():
    idea = request.json["idea"]

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""Write a fun, short story for a 10-year-old about: {idea}

                Make it:
                - Exciting and creative
                - About 150 words
                - Positive and age-appropriate
                - Have a clear beginning, middle, and end"""
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.8,
        max_tokens=500,
    )

    return jsonify({
        "story": chat_completion.choices[0].message.content
    })

if __name__ == "__main__":
    app.run()