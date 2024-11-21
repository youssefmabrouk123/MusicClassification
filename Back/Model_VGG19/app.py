from flask import Flask, request, jsonify
from flask_cors import CORS

import librosa
import numpy as np
import pickle
import os

# Initialize Flask app
app = Flask(__name__)

CORS(app, origins=["http://localhost:1001"])  # Enable CORS for Angular's port

app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Load the SVM model
model_filename = 'svm_genre_classifier.pkl'
with open(model_filename, 'rb') as file:
    clf = pickle.load(file)

# Genres list (ensure it matches the training labels)
genres = ["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"]

# Define the function to predict genre
def predict_genre(file_path, clf):
    hop_length = 512
    n_fft = 2048
    n_mels = 128

    # Load and preprocess the audio file
    signal, rate = librosa.load(file_path)
    S = librosa.feature.melspectrogram(y=signal, sr=rate, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels)
    S_DB = librosa.power_to_db(S, ref=np.max)
    S_DB = S_DB.flatten()[:1200]  # Ensure length matches training input

    # Predict the genre
    genre_label = clf.predict([S_DB])[0]
    return genres[genre_label]

# Define a route for prediction
@app.route('/predict', methods=['POST'])
def predict():
    # Check if a file is uploaded
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    # Save the file to the upload folder
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Predict the genre
    try:
        predicted_genre = predict_genre(filepath, clf)
        result = {'genre': predicted_genre}
    except Exception as e:
        result = {'error': str(e)}

    # Clean up uploaded file
    os.remove(filepath)

    return jsonify(result)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
