from flask import Flask, request, jsonify
from flask_cors import CORS
from auth import init_db, register_user, login_user
from study_plan import generate_plan
from quiz import generate_quiz
from summarizer import summarize
from nlp_tips import tips
from feedback import feedback

app = Flask(__name__)
CORS(app)
init_db()

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    return jsonify({"success": register_user(data["email"], data["password"])})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    return jsonify({"success": login_user(data["email"], data["password"])})

@app.route("/study-plan", methods=["POST"])
def study_plan():
    d = request.json
    return jsonify(generate_plan(d["subject"], d["hours"]))

@app.route("/quiz", methods=["POST"])
def quiz():
    return jsonify(generate_quiz(request.json["topic"]))

@app.route("/summary", methods=["POST"])
def summary():
    return jsonify(summarize(request.json["text"]))

@app.route("/tips", methods=["POST"])
def study_tips():
    return jsonify(tips(request.json["text"]))

@app.route("/feedback", methods=["POST"])
def user_feedback():
    return jsonify(feedback(request.json["score"]))

if __name__ == "__main__":
    app.run()
