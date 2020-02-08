from loadModel import load_model
from imagenet_utils import preprocess_input
from keras.models import Model
from keras.preprocessing import image
import numpy as np
vehicle_classifier=load_model()
def test_type(img_path):
    image=img_preprocess(img_path)
    pred=vehicle_classifier.predict(image)
    return decode_predictions(pred)



def img_preprocess(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    return preprocess_input(x)

def decode_predictions(pred):
     max_val=np.argmax(pred)
     if max_val==0:
         return "Bike"
       
     else:
         return "Car"
         
  
