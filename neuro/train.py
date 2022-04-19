import numpy as np


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