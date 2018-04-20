from naive_bayes_model import NaiveBayesModel


def data_iterator(filename):
    with open(filename, 'r', encoding='utf8') as f:
        for line in f:
            line = line[:-1]
            label, words_str = line.split('@')
            words = words_str.split('#')

            yield words, label


def main():
    # train_iterator = data_iterator('data_set_train.txt')
    dev_iterator = data_iterator('data_set_test.txt')

    model = NaiveBayesModel(['hamidrasaee', 'MJ_Akbarin'])
    # model.train(train_iterator)
    # model.save()

    model.load('model_1523953281')
    result = model.eval(dev_iterator)

    import json
    print(json.dumps(result, indent=4))


if __name__ == '__main__':
    main()
