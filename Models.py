import numpy as np
import tensorflow as tf

class ModelA():
    def __init__(self): 
        self.graph = tf.Graph()
        with self.graph.as_default():
            self.sess = tf.Session()
            self.saver = saver = tf.train.import_meta_graph('Model/saved_model.meta')
            #restore the model
            self.saver.restore(self.sess,tf.train.latest_checkpoint('Model/'))

            self.x= self.graph.get_tensor_by_name("Input:0")
            self.prediction = self.graph.get_tensor_by_name("Prediction:0")
            self.prediction = (tf.nn.softmax(self.prediction))


    def predict(self, image_arr):
        result = (self.sess.run(self.prediction,{self.x:image_arr}))
        return np.argmax(result)


class ModelB():
    def __init__(self):
        self.graph = tf.Graph()
        with self.graph.as_default():
            self.sess = tf.Session()
            self.saver = saver = tf.train.import_meta_graph('Alphabet_Model/saved_model.meta')
            #restore the model
            self.saver.restore(self.sess,tf.train.latest_checkpoint('Alphabet_Model/'))

            self.x= self.graph.get_tensor_by_name("Input:0")
            self.prediction = self.graph.get_tensor_by_name("Prediction:0")
            self.prediction = (tf.nn.softmax(self.prediction))


    def predict(self, image_arr):
        result = (self.sess.run(self.prediction,{self.x:image_arr}))
        index = np.argmax(result)
        return str(chr(65 + index))

