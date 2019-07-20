# MNIST-Tensorflow
MNIST dataset trained using CNN in tensorflow 

The dataset of this project has been downloaded from keras dataset. Then it is trained using convolutional neural network in tensorflow. 

# Dependencies
A system with `anaconda` and `jupyter notebook` installed is required.

### Python packages required
All the required packages can be found in requirements.txt

#### Installation
```shell
git clone https://github.com/shivam197/MNIST-Tensorflow.git
cd MNIST_Tensorflow
pip install -r requirements.txt
```


This project includes :

**1. Image Pre-processing** : Image augmentation has been applied to the images to increase the size of dataset and increase the overall accuracy of model in real life scenarios. Code implementing this can be found in Image Pre-Processing.ipynb where images are rotated 30° in both directions.

**2. Training** : Using the dataset gerenated after image preprocessing, CNN model is trained and accuracy above 99% is achieved. Its implementation can be found in training.ipynb file. 

**3. Flask web application** : Flask web application uses html canvas along with javascript in frontend for drawing digits and bootstrap for styling. It saves the figure drawn on html canvas as Untitled.png and uses saved tensorflow model to make predictions.

#### Running app in development mode
In the project directory, run the following command in conda-prompt:
`python app.py`

Open [http://localhost:5000](http://localhost:5000).

![Webpage_ss](https://user-images.githubusercontent.com/51543033/61583730-aa5a6280-ab59-11e9-8370-b5503a2a4b1b.png)

