from flask import Flask, redirect, url_for, request, render_template, jsonify
from werkzeug.utils import secure_filename
from fastai.vision import *
import cv2
import requests
import pathlib

app = Flask(__name__)


path = './models'

local_cascade_file = os.path.join(path, 'haarcascade_frontalface_default.xml')

if not pathlib.Path(local_cascade_file).exists():
    print('Downloading face cascade...')
    face_cascade_url = 'https://github.com/opencv/opencv/raw/master/data/haarcascades/haarcascade_frontalface_default.xml'
    with open(local_cascade_file, 'wb') as f:
        r = requests.get(face_cascade_url)
        f.write(r.content)

face_cascade = cv2.CascadeClassifier(local_cascade_file)

classes = ['cindy crawford',
'claudia schiffer',
'kate moss',
'kate upton',
'lily cole',
'miranda kerr',
'naomi campbell']

tfms = get_transforms(do_flip=False)

data = ImageDataBunch.single_from_classes(path, classes, ds_tfms=tfms, size=224).normalize(imagenet_stats)
learn = create_cnn(data, models.resnet34)
learn.load('stage-2')
print('Model loaded')

def attempt_face_crop(img_path):
    ''' will overwrite the uploaded image with one cropped on face if possible'''
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    if len(faces) == 1:
        (x,y,w,h) = faces[0]
        cy1 = int(max(0, y - (0.5*h)))
        cy2 = int(min(y + (1.5*h), img.shape[0]))
        cx1 = int(max(0, x - (0.5*w)))
        cx2 = int(min(x + (1.5*w), img.shape[1]))
        cropped_img_padded = img[cy1:cy2, cx1:cx2]
        cv2.imwrite(img_path, cropped_img_padded)

def model_predict(img_path):
    ''' try to predict the class of the image'''
    attempt_face_crop(img_path) # crops to face but only if exactly one face is found
    img = open_image(img_path)
    pred_class, pred_idx, outputs = learn.predict(img)

    results = [(c, p) for c, p in zip(classes, outputs)]
    results.sort(key=lambda x: x[1], reverse=True)
    print(results)
    results = {str(r[0]): '{0:.3f}'.format(r[1]) for r in results[:3]}
    return jsonify(results)


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path)
        return preds
    return None


if __name__ == '__main__':
    app.run(debug=True)