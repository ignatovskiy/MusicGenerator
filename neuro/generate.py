import json
import os
import argparse


import numpy as np
from keras.layers import Activation, Dense, Dropout, Embedding, LSTM
from keras.models import Sequential


INPUT_DIR = './input'
MODEL_DIR = './model'


def create_model(vocabulary_size):

    final_model = Sequential()

    final_model.add(Embedding(vocabulary_size, 512, batch_input_shape=(1, 1)))

    for i in range(3):
        final_model.add(LSTM(256, stateful=True, return_sequences=(i != 2)))
        final_model.add(Dropout(0.2))

    final_model.add(Dense(vocabulary_size))

    final_model.add(Activation('softmax'))

    return final_model


def generate_melody(start_sequence, chars_amount):
    with open(os.path.join(INPUT_DIR, 'char_to_idx.json'), 'w', encoding="UTF-8")\
            as json_file:
        chars_to_id_dict = json.load(json_file)

    vocabulary_size = len(chars_to_id_dict)
    id_to_char_dict = {char_id: char for (char, char_id) in chars_to_id_dict.items()}
    model = create_model(vocabulary_size)

    model.load_weights(os.path.join(MODEL_DIR, 'weights.100.h5'))
    model.save(os.path.join(MODEL_DIR, 'model.100.h5'))

    generated = [chars_to_id_dict[char] for char in start_sequence]
    print(generated)

    for _ in range(chars_amount):

        batch = np.zeros((1, 1))

        if generated:
            batch[0, 0] = generated[-1]

        else:
            batch[0, 0] = np.random.randint(vocabulary_size)

        generated_result = model.predict_on_batch(batch).ravel()
        generated_start = np.random.choice(range(vocabulary_size), p=generated_result)

        generated.append(generated_start)

    header_midi = "M: 3/4\nL: 1/8\nQ: 1/4=100\n"
    sample_text = "".join(id_to_char_dict[char] for char in generated)

    with open('test.abc', 'w', encoding="UTF-8") as f:
        if not sample_text.startswith("M: "):
            f.write(header_midi)

        f.write(sample_text)

        if not sample_text.endswith("]") and not sample_text.endswith("|"):
            f.write("]")

    return sample_text


def main(args_list):
    print(generate_melody(args_list.start, args.len))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate ABC notation for MIDI file.')
    parser.add_argument('--start', default='', help='start characters')
    parser.add_argument('--len', default=256, help='chars amount for generation')
    args = parser.parse_args()

    main(args)
