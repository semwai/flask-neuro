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
    plt.savefig('static/fig1.jpg')
    plt.close()
    #return app.send_static_file('fig1.jpg')
    #return redirect('/index.html?pred=' + np.str(pred))
    return render_template('index.html', photo='fig1.jpg')

"""
model = keras.Sequential(
    [
        keras.Input(shape=input_shape),
        layers.Conv2D(32, kernel_size=(3, 3), activation="relu"), # количество и размер сверточных слоев
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation="softmax"),
    ]
)
"""
