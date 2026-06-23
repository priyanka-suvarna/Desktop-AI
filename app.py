from flask import Flask, request, jsonify, render_template
from assistant import process_command  # Import from our assistant module

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")  # Serve the frontend

@app.route("/assistant", methods=["POST"])
def assistant():
    try:  # Added error handling
        user_input = request.json.get("query")
        if not user_input:
            return jsonify({"error": "No query provided"}), 400
            
        response = process_command(user_input)
        return jsonify({"response": response})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

