from Models import ModelA, ModelB
from flask import Flask, render_template, request
import numpy as np
import re
import base64
import os
import pandas as pd
import tensorflow as tf
from PIL import Image

app = Flask(__name__, static_folder="./static/", template_folder="./templates")

app.config['UPLOADED_PHOTOS_DEST'] = '/Upload'

a = ModelA()
b = ModelB()

digitDf = pd.read_csv("Database/DigitQuestions.csv")
lettersDf = pd.read_csv("Database/LetterQuestions.csv")

def ImageConversion(raw_image):
    img_string = re.search(r'base64,(.*)', raw_image).group(1)
    img_string = bytes(img_string, 'utf-8')
    with open('Upload/Untitled.png', 'wb') as output:
        output.write(base64.decodestring(img_string))


def ImagePreprocessing():
    image = Image.open('Upload/Untitled.png').convert('RGB').convert('L')
    image = image.resize((75, 75))
    arr = np.array(image)

    arr = 255-arr
    while np.sum(arr[0]) == 0:
        arr = arr[1:]
    while np.sum(arr[:, 0]) == 0:
        arr = arr[:, 1:]
    while np.sum(arr[-1]) == 0:
        arr = arr[:-1]
    while np.sum(arr[:, -1]) == 0:
        arr = arr[:, :-1]

    height = arr.shape[0]
    width = arr.shape[1]

    if height > width:
        ratio = height/20
        height = int(height/ratio)
        width = int(width/ratio)

    else:
        ratio = width/20
        height = int(height/ratio)
        width = int(width/ratio)

    image = Image.fromarray(arr)
    image = image.resize((int(width), int(height)))
    arr = np.array(image)

    upr_arr = np.zeros(shape=(14-int(height/2), width))
    height = height + (14-int(height/2))
    lwr_arr = np.zeros(shape=(28-height, width))

    left_arr = np.zeros(shape=(28, 14-int(width/2)))
    width = width + 14-int(width/2)
    right_arr = np.zeros(shape=(28, 28-width))

    arr = np.concatenate((upr_arr, arr, lwr_arr))
    arr = np.concatenate((left_arr, arr, right_arr), axis=1)
    arr = arr.reshape(1, 28, 28, 1)

    return arr


@app.route('/')
def index():
    return render_template("home.html")

@app.route('/', methods = ['POST'])
def captcha():
    captchaType = request.form.get("captchaProcess")
    if captchaType == "ocr":
        questionNo = -1
        questionSet = -1
        questionSet = np.random.randint(2)
        if questionSet == 0:
            questionNo = np.random.randint(len(digitDf)-1)
            question = digitDf["Question"][questionNo]
            additionalMessage = ""
        else:
            questionNo = np.random.randint(len(lettersDf)-1)
            question = lettersDf["Question"][questionNo]
            additionalMessage = "Note: Draw uppercase letter only!"

        return render_template("ocr.html", question=question, message = additionalMessage, questionSet = questionSet, questionNo = questionNo)

    elif captchaType == "checkboard":
        return render_template("checkerboard.html")

    elif captchaType == "spotlight":
        return render_template("spotlight.html")

    elif captchaType == "sliding":
        return render_template("sliding.html")

@app.route('/predict/', methods=['GET', 'POST'])
def predict():
    reponseObtained = request.get_json()

    raw_image = reponseObtained["Image"]

    questionNo = int(reponseObtained["QuestionNo"])

    questionSet = int(reponseObtained["QuestionSet"])

    ImageConversion(raw_image)

    image_arr = ImagePreprocessing()

    if questionSet == 0:
        response = a.predict(image_arr)
    else:
        response = b.predict(image_arr)

    if questionSet == 0:
        expected = digitDf["Answer"][questionNo]
    else:
        expected = lettersDf["Answer"][questionNo]

    print("Expected = " + str(expected) + "\nResponse = " + str(response))
    print("Question Set = " + str(questionSet) + "\nQuestion No = " + str(questionNo))
    if response == expected:
        message = "Captcha verification Successful. Form Submitted."
        return "{}".format("Successful!")
    else:
        message = "Captcha verification FAILED. Form not Submitted."
        return "{}".format("Failed!")

    print("Return render template end page")
    return render_template("endPage.html", message = message)


if __name__ == "__main__":
    app.run()
