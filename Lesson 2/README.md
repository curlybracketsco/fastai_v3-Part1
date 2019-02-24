A web app to which you can upload a photo and the top three results from the trained model will be returned.

The trained model should be a .pth file and goes in models/models

This app also attempts to find and crop to a face (using OpenCV) before passing the input image to the model (hopefully to improve accuracy as the model has been trained on face-cropped images in Lesson 1).

The basic Flask app outline for an app with javascript image upload is from here: https://github.com/shankarj67/Water-classifier-fastai
