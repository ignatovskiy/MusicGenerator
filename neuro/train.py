import numpy as np
import os
import json
import argparse


from utils import create_model, save_weights_to_file


SEQUENCE_SIZE = 64
BATCH_SIZE = 16


def batch_handling(raw_text, vocabulary_size):
    text_size = raw_text.shape[0]
    batches_amount = int(text_size / BATCH_SIZE)

    for i in range(batches_amount - SEQUENCE_SIZE, SEQUENCE_SIZE):
        x = np.zeros((BATCH_SIZE, SEQUENCE_SIZE))
        y = np.zeros((BATCH_SIZE, SEQUENCE_SIZE, vocabulary_size))

        for batch_number in range(BATCH_SIZE):
            for j in range(SEQUENCE_SIZE):
                x[batch_number, i] = raw_text[batches_amount * batch_number + i + j]
                y[batch_number, i, raw_text[batches_amount * batch_number + i + j + 1]] = 1
        yield x, y


DATA_DIR = 'input'


def train(raw_text, weights=10, epochs=100):
    chars_to_id_dict = {char: char_id
                        for (char_id, char)
                        in enumerate(sorted(list(set(raw_text))))}

    print("VOCABULARY SIZE: {}".format(str(len(chars_to_id_dict))))

    with open(os.path.join(DATA_DIR, 'char_to_idx.json'), 'w', encoding="UTF-8")\
            as json_file:
        json.dump(chars_to_id_dict, json_file)

    id_to_char_dict = {char_id: char for (char, char_id) in chars_to_id_dict.items()}

    vocabulary_size = len(chars_to_id_dict)
    model = create_model(BATCH_SIZE, SEQUENCE_SIZE, vocabulary_size)

    model.summary()

    model.compile(optimizer='adam', metrics=['accuracy'], loss='categorical_crossentropy')

    train_data = np.asarray([chars_to_id_dict[char] for char in raw_text], dtype=np.int32)

    print("Text size: {}".format(str(train_data.size)))

    epoch_size = (len(raw_text) / BATCH_SIZE - 1) / SEQUENCE_SIZE

    for epoch in range(epochs):
        losses, accuracies = [], []

        print('\nEpoch {}/{}'.format(epoch + 1, epochs))

        for i, (x, y) in enumerate(batch_handling(train_data, vocabulary_size)):
            loss, accuracy = model.train_on_batch(x, y)

            accuracies.append(accuracy)
            losses.append(loss)

            print("Batch {} - loss: {}, accuracy: {}".format(i + 1, loss, accuracy))

        if (epoch + 1) % epochs == 0:
            print("Saving temp weights to 'weights.{}.h5' file".format(epoch + 1))

            save_weights_to_file(epoch + 1, model)


def main(args_line):
    with open(os.path.join(DATA_DIR, args_line.input), 'r', encoding="UTF-8") as inp_f:
        input_data = inp_f.read()

    train(input_data, args_line.epochs, args_line.save)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Training models.')

    parser.add_argument('--input', default='input.txt', help='input file with text data')
    parser.add_argument('--epochs', default=100, help='epochs for training')
    parser.add_argument('--save', default=10, help='save weights every {} epochs')

    args = parser.parse_args()

    main(args)
