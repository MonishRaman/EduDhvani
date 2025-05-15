from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, flash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "edudhvani_secret"
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Dummy data for states, grades, subjects, chapters
STATES = ["Maharashtra", "Tamil Nadu", "West Bengal"]
GRADES = ["6", "7", "8", "9", "10"]
SUBJECTS = {
    "Maharashtra": ["Math", "Science", "Marathi"],
    "Tamil Nadu": ["Math", "Science", "Tamil"],
    "West Bengal": ["Math", "Science", "Bengali"]
}
CHAPTERS = {
    "Math": ["Numbers", "Algebra", "Geometry"],
    "Science": ["Plants", "Animals", "Physics"],
    "Marathi": ["Kavita", "Vyakaran"],
    "Tamil": ["Kavithai", "Ilakkanam"],
    "Bengali": ["Kabita", "Byakaran"]
}

@app.route("/", methods=["GET", "POST"])
def onboarding():
    if request.method == "POST":
        session['name'] = request.form['name']
        session['school_type'] = request.form['school_type']
        session['state'] = request.form['state']
        session['grade'] = request.form['grade']
        return redirect(url_for('dashboard'))
    return render_template("onboarding.html", states=STATES, grades=GRADES)

@app.route("/dashboard")
def dashboard():
    state = session.get('state')
    subjects = SUBJECTS.get(state, [])
    return render_template("dashboard.html", name=session.get('name'), subjects=subjects)

@app.route("/module/<subject>")
def module(subject):
    chapters = CHAPTERS.get(subject, [])
    return render_template("module.html", subject=subject, chapters=chapters)

@app.route("/quiz/<subject>/<chapter>", methods=["GET", "POST"])
def quiz(subject, chapter):
    # Dummy quiz
    questions = [
        {"q": f"What is 2+2 in {subject}?", "a": "4"},
        {"q": f"Name a topic in {chapter}.", "a": chapter}
    ]
    feedback = None
    if request.method == "POST":
        answers = [request.form.get(f"q{i}") for i in range(len(questions))]
        correct = sum(1 for i, ans in enumerate(answers) if ans and ans.strip().lower() == questions[i]["a"].lower())
        feedback = f"You got {correct}/{len(questions)} correct!"
    return render_template("quiz.html", subject=subject, chapter=chapter, questions=questions, feedback=feedback)

@app.route("/doubt", methods=["GET", "POST"])
def doubt():
    if request.method == "POST":
        if 'voice' in request.files:
            f = request.files['voice']
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash("Doubt submitted successfully!", "success")
            return redirect(url_for('doubt'))
    return render_template("doubt.html")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# PWA manifest and service worker
@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')

@app.route('/service-worker.js')
def service_worker():
    return send_from_directory('static', 'service-worker.js')

if __name__ == "__main__":
    app.run(debug=True)
