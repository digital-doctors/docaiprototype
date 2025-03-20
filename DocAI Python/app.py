from flask import Flask, render_template, request, jsonify
import random
import time
import cohere

app = Flask(__name__)

# Initialize Cohere AI
COHERE_API_KEY = "oaiXjisZYMP0ZrNLdEHKSPduxKpJSIKZLAzIJ2aZ"  # Replace with your actual key
co = cohere.Client(COHERE_API_KEY)

# Route for homepage
@app.route('/')
def home():
    return render_template('index.html')

# Route for health analysis (Simulated but Feels Real)
@app.route('/analyze')
def analyze():
    time.sleep(3)  # Simulate processing delay

    health_data = {
        "heart_rate": f"{random.randint(65, 100)} BPM",
        "hydration": random.choice(["Normal", "Mild Dehydration", "Severe Dehydration"]),
        "temperature": f"{round(random.uniform(97.0, 99.5), 1)} °F",
        "blood_pressure": f"{random.randint(110, 135)}/{random.randint(70, 90)} mmHg"
    }
    return jsonify(health_data)

# AI-Generated Health Report using Cohere
@app.route('/report', methods=['POST'])
def report():
    data = request.get_json()
    
    query = (
        f"Generate a professional health report based on the following:\n"
        f"- Heart Rate: {data['heart_rate']}\n"
        f"- Hydration Status: {data['hydration']}\n"
        f"- Temperature: {data['temperature']}\n"
        f"- Blood Pressure: {data['blood_pressure']}\n\n"
        f"Provide insights and recommendations in a clear and helpful way."
    )

    try:
        response = co.chat(
            message=query,
            model="command-light",
            temperature=0.7
        )
        ai_report = response.text
    except Exception as e:
        ai_report = f"Error fetching AI-generated report: {str(e)}"

    return jsonify({"report": ai_report})

if __name__ == '__main__':
    app.run(debug=True)
