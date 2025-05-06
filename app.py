from flask import Flask, request, jsonify
import easyocr
import cv2
import numpy as np

app = Flask(__name__)

# Initialize EasyOCR Reader
reader = easyocr.Reader(['en'])

@app.route('/process-image', methods=['POST'])
def process_image():
    try:
        # Check if an image is included in the request
        if 'image' not in request.files:
            return jsonify({"error": "No image file uploaded"}), 400

        # Read the uploaded image
        file = request.files['image']
        image = np.frombuffer(file.read(), np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        # Extract text using EasyOCR
        results = reader.readtext(image)

        # Format the response
        text_results = [{"text": text, "confidence": prob} for (_, text, prob) in results]
        return jsonify({"data": text_results}), 200

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    # Run the Flask app locally
    app.run(host='0.0.0.0', port=5000)
