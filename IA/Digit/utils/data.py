import numpy
import scipy
import skimage
from sklearn.datasets import * # chargement du package datasets contenant plusieurs jeu de données
import pandas as pd # Chargement de Pandas
import matplotlib.pyplot as plt # import de Matplotlib
from sklearn.model_selection import train_test_split # classe utilitaire pour découper les jeux de données
from sklearn.neighbors import KNeighborsClassifier

IMG_SIZE = 28
IMG_SHAPE = (IMG_SIZE, IMG_SIZE)
IMG_CENTER_SIZE = 20
NUM_CLASSES = 10
NUM_PROCESS_STEPS = 4

def get_train_data_test_data():
    
    digit = load_digits() # chargement du dataset MNIST
    dig = pd.DataFrame(digit['data'][0:1700]) # Création d'un dataframe Panda
    train_x = digit.data
    train_y =  digit.target
    x_train,x_test,y_train,y_test=train_test_split(train_x,train_y,test_size=0.25)
    return x_train,x_test,y_train,y_test

def format_x(x):
    x = numpy.array(x)
    x = x.astype("float32")
    if numpy.max(x)>0:
        x /=numpy.max(x)        
    x *= 16
    return x
