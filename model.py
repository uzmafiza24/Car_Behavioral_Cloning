## File: model.py
## Name: Manuel Cuevas
## Date: 02/14/2017
## Project: CarND - Behavioral Cloning
## Desc: convolution neural network model to learn a track
## Ref: https://devblogs.nvidia.com/parallelforall/deep-learning-self-driving-cars/
#######################################################################################
'''
This model was based on the Nvidia model with modification to better fit our needs
This model uses 5 convolutional layers with filter size 5x5, 5x5, 5X5, 3x3, 3x3 followed by a
elu activations.
Input:  160, 320, 3
Return: logits'''
from keras.layers.convolutional import Convolution2D, Cropping2D, ZeroPadding2D
from keras.layers.pooling import MaxPooling2D
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Flatten, Reshape, Dropout
from keras.layers.pooling import MaxPooling2D, AveragePooling2D
from keras.layers import Lambda, ELU

def get_model():
    model = Sequential()
    
    # Preprocess incoming data
    # Normalize the features using Min-Max scaling centered around zero and reshape
    model.add(Lambda(lambda x: (x/125.5) - 1., input_shape=(160, 320, 3), output_shape=(160, 320, 3)))
    # Image is crop to left only the important features of the image
    model.add(Cropping2D(cropping=((70,25),(0,0))))

    model.add(Convolution2D(24, 5, 5, subsample=(4, 4), border_mode="same"))
    model.add(ELU())
    model.add(Convolution2D(36, 5, 5, subsample=(2, 2), border_mode="same"))
    model.add(ELU())
    model.add(Convolution2D(48, 5, 5, subsample=(2, 2), border_mode="same"))
    model.add(ELU())
    model.add(Convolution2D(64, 3, 3, subsample=(2, 2), border_mode="same"))
    model.add(ELU())
    model.add(Convolution2D(64, 3, 3, subsample=(2, 2), border_mode="same"))

    model.add(Flatten())
    model.add(Dropout(.2))
    model.add(ELU())

    model.add(Dense(1164))
    model.add(Dropout(.2))
    model.add(ELU())

    model.add(Dense(100))
    model.add(Dropout(.2))
    model.add(ELU())

    model.add(Dense(50))
    model.add(Dropout(.5))
    model.add(ELU())

    model.add(Dense(10))
    model.add(Dropout(.5))
    model.add(ELU())

    model.add(Dense(1))
    # compile model using adam
    model.compile(optimizer="adam", loss="mse")
    return model

'''
Stores the trained model to json format
Input:  model - trained model
        location, - folder location
Return: void '''
def savemodel(model, location = "./steering_model"):
    import os
    import json
    print("Saving model weights and configuration file.")

    if not os.path.exists(location):
        os.makedirs(location)

    # serialize model to JSON and weights to h5
    model.save_weights(location + "/model.h5", True)
    with open(location +'/model.json', 'w') as outfile:
        outfile.write(model.to_json())
        
    print("Saved model to disk")






