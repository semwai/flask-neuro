from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
from flask import send_file
from matplotlib import image
import matplotlib.pyplot as plt
import numpy as np 
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import load_model

app = Flask(__name__)

model = load_model('model.h5')

@app.route('/')
def hello_world():
    return render_template('index.html', name='semwai!!')

@app.route('/load', methods=['POST'])
def get_image():
    f = request.files['image']
        
     
    img_source = image.imread(f) # 28 * 28 
    img = img_source.astype(np.float32)
    img = [[ [img[i][j][0] + img[i][j][1] + img[i][j][2]] for j in range(28)] for i in range(28)] 
    n = np.array([img]) / (255*3)

    

    pred = np.argmax(model.predict(n))
    print(pred)
    plt.imshow(img_source)
    plt.title(f"Я думаю это число %d" % (pred))
    plt.axis('off')
    imgName = 'out/fig' + np.str(np.random.rand())[2:] + '.jpg'
    plt.savefig('static/' + imgName)
    plt.close()
    return render_template('index.html', photo=imgName)
 