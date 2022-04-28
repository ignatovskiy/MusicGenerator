from keras.layers import Activation, Dense, Dropout, Embedding, LSTM
from keras.models import Sequential


def build_model(vocabulary_size):

    final_model = Sequential()

    final_model.add(Embedding(vocabulary_size, 512, batch_input_shape=(1, 1)))

    for i in range(3):
        final_model.add(LSTM(256, stateful=True, return_sequences=(i != 2)))
        final_model.add(Dropout(0.2))

    final_model.add(Dense(vocabulary_size))

    final_model.add(Activation('softmax'))

    return final_model
