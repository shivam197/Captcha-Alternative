
from flask import Flask, render_template,request
import numpy as np
import re
import base64
import os
import tensorflow as tf
from PIL import Image

app = Flask(__name__)
app.config['UPLOADED_PHOTOS_DEST'] = '/Upload'

sess= tf.Session()
saver= tf.train.import_meta_graph('Model/saved_model.meta')
saver.restore(sess,tf.train.latest_checkpoint('Model/'))

graph = tf.get_default_graph()
x= graph.get_tensor_by_name("Input:0")
#keep_prob = graph.get_tensor_by_name("keep_prob:0")
prediction = graph.get_tensor_by_name("Prediction:0")
prediction = (tf.nn.softmax(prediction))

def ImageConversion(raw_image):

	raw_image = raw_image.decode('utf-8')
	img_string = re.search(r'base64,(.*)',raw_image).group(1)
	img_string = bytes(img_string,'utf-8')
	with open('Upload/Untitled.png','wb') as output:
		output.write(base64.decodestring(img_string))


def ImagePreprocessing():

	image = Image.open('Upload/Untitled.png').convert('RGB').convert('L')
	image = image.resize((75,75))
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

	left_arr = np.zeros(shape=(28,14-int(width/2)))
	width = width + 14-int(width/2)
	right_arr = np.zeros(shape=(28,28-width))

	arr = np.concatenate((upr_arr,arr,lwr_arr))
	arr = np.concatenate((left_arr,arr,right_arr),axis=1)
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
