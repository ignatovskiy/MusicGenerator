import os


MODELS_FOLDER = './model'


def load_weights_from_file(temp_model, epochs=100):
    temp_model.load_weights(os.path.join(MODELS_FOLDER, 'weights.{}.h5'.format(epochs)))


def save_weights_to_file(temp_model, epochs=100):
    if not os.path.exists(MODELS_FOLDER):
        os.makedirs(MODELS_FOLDER)

    temp_model.save_weights(os.path.join(MODELS_FOLDER, "weights.{}.h5".format(epochs)))


