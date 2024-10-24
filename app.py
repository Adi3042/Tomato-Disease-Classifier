from __future__ import division, print_function
import sys
import os
import numpy as np
import tensorflow as tf

# Keras
from tensorflow.keras.applications.vgg16 import preprocess_input, VGG16
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.utils import get_custom_objects
from flask import Flask, request, render_template, send_from_directory
from werkzeug.utils import secure_filename

# Define a Flask app
app = Flask(__name__)

MODEL_PATH = 'D:\\Tomato-Leaf-Disease-Prediction\\model_vgg16.h5'

try:
    model = load_model(MODEL_PATH)
except ValueError as e:
    print(f"Error loading model: {e}")

# Define your class labels
CLASS_LABELS = [
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy"
]

# Define shortened names for user-friendly display
SHORT_CLASS_LABELS = [
    "Bacterial Spot",
    "Early Blight",
    "Late Blight",
    "Leaf Mold",
    "Septoria Spot",
    "Spider Mites",
    "Target Spot",
    "Yellow Leaf Curl Virus",
    "Tomato Mosaic Virus",
    "Healthy"
]

def model_predict(img_path, model):
    print(img_path)
    img = image.load_img(img_path, target_size=(224, 224))

    # Preprocessing the image
    x = image.img_to_array(img)
    x = x / 255.0  # Normalize the image to the range [0,1]
    x = np.expand_dims(x, axis=0)

    # Make predictions
    preds = model.predict(x)
    preds = np.argmax(preds, axis=1)

    # Map predictions to short class labels
    result = SHORT_CLASS_LABELS[preds[0]] if preds.size > 0 else "Unknown Disease"
    
    print("\n\npreds: ", result)
    return result

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

@app.route('/predict', methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        if not f:
            return {'result': 'No file uploaded'}, 400

        basepath = os.path.dirname(__file__)
        uploads_path = os.path.join(basepath, 'uploads')
        if not os.path.exists(uploads_path):
            os.makedirs(uploads_path)  # Create uploads directory if it doesn't exist

        file_path = os.path.join(uploads_path, secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        
        # Return both the prediction and image path
        return {'result': preds, 'image_path': f.filename}
    return None


if __name__ == '__main__':
    app.run(port=5001, debug=True)
