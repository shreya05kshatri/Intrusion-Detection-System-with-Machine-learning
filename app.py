from flask import Flask, request, render_template, jsonify, Response
import joblib
import numpy as np
import pandas as pd  # ✅ added
import queue
import time

app = Flask(__name__)

# Load model and encoders
model = joblib.load("random_forest_ids_model.pkl")
encoders = joblib.load("label_encoders.pkl")

# Real-time prediction queue
prediction_queue = queue.Queue()

@app.route('/')
def index():
    return render_template('index.html')

# Web form submission
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Input from form
        duration = float(request.form['duration'])
        protocol_type = request.form['protocol_type']
        service = request.form['service']
        flag = request.form['flag']
        src_bytes = float(request.form['src_bytes'])
        dst_bytes = float(request.form['dst_bytes'])
        count = float(request.form['count'])

        # Encode
        protocol_type_encoded = encoders['protocol_type'].transform([protocol_type])[0]
        service_encoded = encoders['service'].transform([service])[0]
        flag_encoded = encoders['flag'].transform([flag])[0]

        # ✅ Use DataFrame with feature names
        input_df = pd.DataFrame([{
            'duration': duration,
            'protocol_type': protocol_type_encoded,
            'service': service_encoded,
            'flag': flag_encoded,
            'src_bytes': src_bytes,
            'dst_bytes': dst_bytes,
            'count': count
        }])

        prediction = model.predict(input_df)[0]
        result = "🚨 Intrusion Detected!" if prediction == 1 else "✅ Normal Traffic"
        return render_template('index.html', prediction_text=result)

    except Exception as e:
        return f"Error: {str(e)}"

# API for packet sniffer to post predictions
@app.route('/predict_api', methods=['POST'])
def predict_api():
    try:
        data = request.get_json()

        duration = float(data['duration'])
        protocol_type = data['protocol_type']
        service = data['service']
        flag = data['flag']
        src_bytes = float(data['src_bytes'])
        dst_bytes = float(data['dst_bytes'])
        count = float(data['count'])

        # Encode
        protocol_type_encoded = encoders['protocol_type'].transform([protocol_type])[0]
        service_encoded = encoders['service'].transform([service])[0]
        flag_encoded = encoders['flag'].transform([flag])[0]

        # ✅ Use DataFrame with feature names
        input_df = pd.DataFrame([{
            'duration': duration,
            'protocol_type': protocol_type_encoded,
            'service': service_encoded,
            'flag': flag_encoded,
            'src_bytes': src_bytes,
            'dst_bytes': dst_bytes,
            'count': count
        }])

        prediction = model.predict(input_df)[0]
        result = "🚨 Intrusion Detected!" if prediction == 1 else "✅ Normal Traffic"

        # Add to live stream queue
        prediction_queue.put(result)

        return jsonify({'prediction': result})

    except Exception as e:
        return jsonify({'error': str(e)})

# SSE route for real-time streaming
@app.route('/stream')
def stream():
    def event_stream():
        while True:
            try:
                result = prediction_queue.get(timeout=10)
                yield f"data: {result}\n\n"
            except queue.Empty:
                yield "data: \n\n"
    return Response(event_stream(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
