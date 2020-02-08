from keras.models import model_from_json
from keras.models import Model

def load_model():
    json_file = open('custom_resnet_model2.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)

# load weights into new model
    loaded_model.load_weights("custom_resnet_model2.h5")
    print("Loaded model from disk")
#compile the model loaded
    loaded_model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
#Evaluate
    #(loss, accuracy) = loaded_model.evaluate(X_test, y_test, batch_size=10, verbose=1)
    return loaded_model
