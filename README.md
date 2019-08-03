# MNIST-Tensorflow
MNIST dataset trained using CNN in tensorflow

The dataset of this project has been downloaded from keras dataset. Then it is trained using convolutional neural network in tensorflow.

# Dependencies
A system with `anaconda` and `jupyter notebook` installed is required.

### Python packages required

`tensorflow==1.14.0`

`Flask==1.1.1`

`Pillow==6.1.0`

`pandas==0.24.2`


This project includes :

**1. Image Pre-processing** : Image augmentation has been applied to the images to increase the size of dataset and increase the overall accuracy of model in real life scenarios. Code implementing this can be found in Image Pre-Processing.ipynb where images are rotated 30° in both directions.
![Untitled](https://user-images.githubusercontent.com/51543033/61584467-bfd58980-ab65-11e9-998f-0042d46df9a1.png)


**2. Training** : Using the dataset gerenated after image preprocessing, CNN model is trained and accuracy above 99% is achieved. Its implementation can be found in training.ipynb file.

**3. Flask web application** : Flask web application uses html canvas along with javascript in frontend for drawing digits and bootstrap for styling. It saves the figure drawn on html canvas as Untitled.png and uses saved tensorflow model to make predictions.

#### Running app in development mode
In the project directory, run the following command in conda-prompt:
`python app.py`

Open [http://localhost:5000](http://localhost:5000).

![ezgif com-video-to-gif](https://user-images.githubusercontent.com/51543033/61825551-38965780-ae7e-11e9-8d28-58d56667ab1a.gif)

This web app deployed on heroku is available at : 

https://fathomless-shore-48898.herokuapp.com
