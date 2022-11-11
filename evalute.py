import tensorflow as tf
import json
from keras.models import load_model


def load_dronet():
    # Load in json and create model
    config = open("model/dronet_config.json")
    config_dict = json.dumps(config.read())
    content = json.loads(config_dict)
    model = tf.keras.models.model_from_json(content)
    model.load_weights("model/dronet_weights.h5")
    return model 


model = load_dronet()
print(model.summary())
