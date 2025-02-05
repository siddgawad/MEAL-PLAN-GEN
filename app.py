from flask import Flask, request, jsonify, render_template
import subprocess

app = Flask(__name__)

@app.route("/")  
def home():
    return render_template("index.html")

@app.route("/about")  # ✅ Fix: Add route for About page
def about():
    return render_template("about.html")

@app.route("/blog")  # ✅ Fix: Add route for Blog page
def blog():
    return render_template("blog.html")

@app.route("/contact")  # ✅ Fix: Add route for Contact page
def contact():
    return render_template("contact.html")

def generate_meal_plan(prompt):
    """Runs the Ollama model locally."""
    result = subprocess.run(["ollama", "run", "siddgawad/MEAL-PLAN", prompt], capture_output=True, text=True)
    return result.stdout.strip()

@app.route("/meal-plan", methods=["POST"])
def meal_plan():
    data = request.json
    if not all(k in data for k in ["age", "dietary_preference", "health_conditions"]):
        return jsonify({"error": "Missing required fields"}), 400

    user_prompt = f"Generate a 7-day meal plan for a {data['age']}-year-old {data['dietary_preference']} with {data['health_conditions']}."
    response = generate_meal_plan(user_prompt)
    return jsonify({"meal_plan": response})

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
