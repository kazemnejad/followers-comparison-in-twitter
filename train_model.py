import json
import os

import pickle

import numpy as np
import tensorflow as tf
from collections import Counter

from model import SingleCNNText, Config
from utils import minibatches, one_hot


def get_data_set(path):
    with open(path, 'r', encoding='utf8') as f:
        data_set = json.load(f)

    for document, label in data_set:
        yield (document, (0 if label == 'MJ_Akbarin' else 1))


def get_data_set_tiny(path):
    with open(path, 'r', encoding='utf8') as f:
        for line in f:
            line = line[:-1]
            label, words_str = line.split('@')
            o_label = 0 if label == 'MJ_Akbarin' else 1
            yield (words_str.split('#'), o_label)


def create_vocabulary(data_path):
    data = get_data_set_tiny('data/data_set.txt')
    save_path = 'data/data_vocab_from_' + data_path.replace('/', '_')
    if os.path.isfile(save_path):
        with open(save_path, 'rb') as handle:
            return pickle.load(handle)

    readed_data = []
    counter = Counter()
    for (words, label) in data:
        counter.update(words)
        readed_data.append((words))

    word_id = 2
    vocab = {}
    vocab['<NULL>'] = 0
    vocab['<UNK>'] = 1
    for (words) in readed_data:
        for w in words:
            if w not in vocab and counter[w] > 5:
                vocab[w] = word_id
                word_id += 1

    with open(save_path, 'wb') as handle:
        pickle.dump(vocab, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return vocab


def load_embedding():
    with open('data/word_vectors', 'rb') as handle:
        params = pickle.load(handle)

    return params['embd'].astype(np.float32), params['words'], params['ids']


def train():
    use_static = True

    config = Config()
    config.use_static = use_static

    if use_static:
        train = get_data_set('data/data_set_train.json')
        dev = get_data_set('data/data_set_dev.json')
        embd, _, word_to_id = load_embedding()
    else:
        train = get_data_set_tiny('data/data_set_train.txt')
        dev = get_data_set_tiny('data/data_set_dev.txt')
        vocab = create_vocabulary('data/data_set.txt')
        config.vocabulary_size = len(vocab)
        config.embedding_size = 100

    with tf.Graph().as_default():
        if use_static:
            model = SingleCNNText(config, embeddings=embd, word_to_id=word_to_id)
        else:
            model = SingleCNNText(config, vocab=vocab)

        init = tf.global_variables_initializer()
        saver = tf.train.Saver()
        tf.summary.scalar('loss', model.loss)

        with tf.Session() as session:
            session.run(init)
            train_writer = tf.summary.FileWriter(model.config.log_output, session.graph)
            model.fit(session, saver, train, dev)

        train_writer.close()


def evaluate():
    dev = get_data_set('data/data_set_dev.json')
    embd, _, word_to_id = load_embedding()

    with tf.Graph().as_default():
        model = SingleCNNText(Config('results/20180420_003353/'), embd, word_to_id)

        init = tf.global_variables_initializer()
        saver = tf.train.Saver()

        with tf.Session() as session:
            session.run(init)
            saver.restore(session, model.config.model_output)

            result = model.evaluate(session, dev)

            import json
            print(json.dumps(result))


if __name__ == '__main__':
    # evaluate()
    # vocab = create_vocabulary('data/data_set.txt')
    # print(len(vocab)
    train()
    # inputs = [
    #     (np.arange(10), one_hot(2, 1)),
    #     (np.arange(10), one_hot(2, 1)),
    #     (np.arange(10), one_hot(2, 1)),
    #     (np.arange(10), one_hot(2, 1)),
    #     (np.arange(10), one_hot(2, 1)),
    #     (np.arange(10), one_hot(2, 1)),
    #     (np.arange(10), one_hot(2, 1)),
    #     (np.arange(10), one_hot(2, 1)),
    # ]
    #
    # for i, (input_batch, label_batch) in enumerate(minibatches(inputs, 3, shuffle=False)):
    #     print(i, input_batch, label_batch)
    #     print("####")
