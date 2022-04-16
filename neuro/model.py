import os

from keras.layers import Activation, Dense, Dropout, Embedding, LSTM, TimeDistributed
from keras.models import load_model, Sequential


MODELS_FOLDER = './model'


def load_weights_from_file(temp_model, epochs=100):
    temp_model.load_weights(os.path.join(MODELS_FOLDER, 'weights.{}.h5'.format(epochs)))


def save_weights_to_file(temp_model, epochs=100):
    if not os.path.exists(MODELS_FOLDER):
        os.makedirs(MODELS_FOLDER)

    temp_model.save_weights(os.path.join(MODELS_FOLDER, "weights.{}.h5".format(epochs)))


def create_model(batch_size, sequence_len, vocabulary_size):
    temp_model = Sequential()

    temp_model.add(Embedding(vocabulary_size, 512, batch_input_shape=(batch_size, sequence_len)))

    for _ in range(3):
        temp_model.add(LSTM(256, stateful=True, return_sequences=True))
        temp_model.add(Dropout(0.2))

    temp_model.add(TimeDistributed(Dense(vocabulary_size)))
    temp_model.add(Activation('softmax'))

    return temp_model

