# -*- coding: utf-8 -*-
import json
import pickle

from tf_glove import GloVeModel


def load_corpus():
    with open('sentences.txt', 'r', encoding='utf8') as f:
        corpus = json.load(f)

    return corpus


def save_model(model):
    model_to_save = {
        "embd": model.embeddings,
        "words": model.words,
        "ids": model.word_ids
    }

    with open('model', 'wb') as handle:
        pickle.dump(model_to_save, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_model(filename):
    with open(filename, 'rb') as handle:
        params = pickle.load(handle)

    return params['embd'], params['words'], params['ids']


def test_model(filename):
    embd, _, ids = load_model(filename)
    print(type(embd), type(ids))
    print(embd.shape)
    print(embd[10])


def main():
    print("# reading corpus...")
    corpus = load_corpus()
    print("# done reading corpus!")
    model = GloVeModel(embedding_size=200, context_size=5,
                       learning_rate=0.05, batch_size=512, max_vocab_size=1000000)

    print("# fitting corpus...")
    model.fit_to_corpus(corpus)
    print("# start fitting corpus!")
    print("# start training...")
    model.train(num_epochs=50, log_dir='logs', on_epoch_finished=lambda: save_model(model))
    print("# done training!")

    print(model.embedding_for("سلام"))
    model.generate_tsne(path='outputs/pic.png')


if __name__ == '__main__':
    test_model('data/word_vectors')
    # main()
