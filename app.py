
from flask import Flask, render_template,request
import numpy as np
import re
import base64
import os
import tensorflow as tf
from PIL import Image

app = Flask(__name__)


sess= tf.Session()
saver= tf.train.import_meta_graph('Model/saved_model.meta')
saver.restore(sess,tf.train.latest_checkpoint('Model/'))

graph = tf.get_default_graph()
x= graph.get_tensor_by_name("Input:0")
prediction = graph.get_tensor_by_name("Prediction:0")
prediction = (tf.nn.softmax(prediction))

def ImageConversion(raw_image):

	raw_image = raw_image.decode('utf-8')
	img_string = re.search(r'base64,(.*)',raw_image).group(1)
	img_string = bytes(img_string,'utf-8')
	with open('Untitled.png','wb') as output:
		output.write(base64.decodestring(img_string))


def ImagePreprocessing():

	image = Image.open('Untitled.png').convert('RGB').convert('L')
	arr = np.array(image)


	arr = 255-arr
	while np.sum(arr[0])==0:
	    arr = arr[1:]
	while np.sum(arr[:,0])==0:
	    arr = arr[:,1:]
	while np.sum(arr[-1])==0:
	    arr = arr[:-1]
	while np.sum(arr[:,-1])==0:
	    arr = arr[:,:-1]
	arr = arr/255
	image = Image.fromarray(arr)
	image = image.resize((20,20))
	arr = np.array(image)
	arr = np.lib.pad(arr,pad_width=4,mode='constant')

	arr = arr.reshape(1,28,28,1)

	return arr
@app.route('/')
def index():
	return render_template("index.html")

@app.route('/predict/',methods=['GET','POST'])
def predict():
	raw_image = request.get_data()

	ImageConversion(raw_image)

	image_arr  = ImagePreprocessing()

	pred = (sess.run(prediction,{x:image_arr}))
	index = np.argmax(pred)
	S = str(index) +"  Probability : " + str(pred[0][index])
	return '{}'.format(S)

if __name__ == "__main__":
	app.run()
