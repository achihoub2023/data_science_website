import tensorflow as tf
import numpy as np
import os
import tensorflow as tf

def model(input_img):

    #print(input_img.shape)
    model = tf.keras.applications.MobileNet(input_shape=(224,224,3),include_top=True,weights='imagenet')
    predictions = model.predict(input_img)
    #print(predictions)
    finals = tf.keras.applications.mobilenet.decode_predictions(
        predictions, top=1
    )
    return finals[0][0][1]