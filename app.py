from flask import Flask, render_template, request, redirect, url_for, Response, send_file
from matplotlib import image
import matplotlib.pyplot as plt
import numpy as np 
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import load_model
from PIL import Image

app = Flask(__name__)

model = load_model('model.h5')

@app.route('/')
def hello_world():
    return render_template('index.html', name='semwai!!')

@app.route('/load', methods=['POST'])
def get_image():
    #try:
    #f = #image.imread(request.files['image'])
        
    img, img_data = normalizeImage(request.files['image'])
    n = np.array([img_data]) 

    pred = np.argmax([model.predict(n)])
    plt.imshow(img, cmap='gray')
    plt.title(f"Я думаю это число %d" % (pred))
    plt.axis('off')
    imgName = 'out/fig' + np.str(np.random.rand())[2:] + '.jpg'
    plt.savefig('static/' + imgName)
    plt.close()
    return 'static/' + imgName
    #except Exception as e:
    #    return Response(str(e), status=500)
        #return "static/out/fig3870747312784326.jpg"


def normalizeImage(file):
    img_source = Image.open(file)
    img_source = img_source.resize((28,28))
    img = np.array([[img_source.getdata()[(i*28 + j)][0] + img_source.getdata()[(i*28 + j)][1] + img_source.getdata()[(i*28 + j)][2] for j in range(28)] for i in range(28)]) / (3 * 255)
    img_data = [[ [img[i][j]] for j in range(28)] for i in range(28)]
    return img, img_data