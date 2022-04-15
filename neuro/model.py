import os


MODELS_FOLDER = './model'


def load_weights_from_file(temp_model, epochs=100):
    temp_model.load_weights(os.path.join(MODELS_FOLDER, 'weights.{}.h5'.format(epochs)))
