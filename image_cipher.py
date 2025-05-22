import os
from flask import Flask, render_template, request, send_from_directory
from PIL import Image # type: ignore

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
ENCRYPTED_FOLDER = 'encrypted'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENCRYPTED_FOLDER, exist_ok=True)

def encrypt_image(image_path, output_path):
    img = Image.open(image_path)
    pixels = img.load()

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            r, g, b = pixels[i, j]
            pixels[i, j] = (255 - r, 255 - g, 255 - b)  # Invert RGB
    img.save(output_path)

def decrypt_image(image_path, output_path):
    encrypt_image(image_path, output_path)  # Inversion is reversible

@app.route('/', methods=['GET', 'POST'])
def index():
    encrypted_filename = decrypted_filename = None

    if request.method == 'POST':
        file = request.files['image']
        action = request.form['action']
        filename = file.filename
        path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(path)

        output_filename = f"{action}_{filename}"
        output_path = os.path.join(ENCRYPTED_FOLDER, output_filename)

        if action == 'encrypt':
            encrypt_image(path, output_path)
            encrypted_filename = output_filename
        elif action == 'decrypt':
            decrypt_image(path, output_path)
            decrypted_filename = output_filename

    return render_template('index.html',
                           encrypted=encrypted_filename,
                           decrypted=decrypted_filename)

@app.route('/encrypted/<filename>')
def serve_file(filename):
    return send_from_directory(ENCRYPTED_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)