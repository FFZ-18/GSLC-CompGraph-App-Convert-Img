from flask import Flask, render_template, request, send_file
import numpy as np
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Halaman utama untuk upload gambar
@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        file = request.files['image']
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            option = request.form['option']  # Grayscale atau Blur

            if option == 'grayscale':
                output_path = convert_to_grayscale(filepath)
            elif option == 'blur':
                output_path = apply_blur(filepath)

            return render_template('result.html', original=filepath, edited=output_path)

    return render_template('upload.html')

# Fungsi convert grayscale
def convert_to_grayscale(image_path):
    img = Image.open(image_path)
    arr = np.array(img)
    grayscale_arr = np.mean(arr[:, :, :3], axis=2).astype(np.uint8)
    grayscale_img = Image.fromarray(grayscale_arr)
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'grayscale.png')
    grayscale_img.save(output_path)
    return output_path

# Fungsi efek blur
def apply_blur(image_path):
    img = Image.open(image_path)
    arr = np.array(img)
    kernel_size = 5
    pad_width = kernel_size // 2
    padded_arr = np.pad(arr, ((pad_width, pad_width), (pad_width, pad_width), (0, 0)), mode='edge')

    blurred_arr = np.zeros_like(arr)
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            for k in range(3):
                blurred_arr[i, j, k] = np.mean(
                    padded_arr[i:i + kernel_size, j:j + kernel_size, k]
                )
    blurred_img = Image.fromarray(blurred_arr)
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'blur.png')
    blurred_img.save(output_path)
    return output_path

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
