from naive_bayes_model import NaiveBayesModel


def data_iterator(filename):
    with open(filename, 'r', encoding='utf8') as f:
        for line in f:
            line = line[:-1]
            label, words_str = line.split('@')
            words = words_str.split('#')

            yield words, label


def train():
    train_iterator = data_iterator('data_set_train.txt')

    model = NaiveBayesModel(['hamidrasaee', 'MJ_Akbarin'])
    model.train(train_iterator)
    model.save()


def evaluate():
    dev_iterator = data_iterator('data_set_test.txt')

    model = NaiveBayesModel(['hamidrasaee', 'MJ_Akbarin'])
    model.load('model_1523953281')
    result = model.eval(dev_iterator)

    import json
    print(json.dumps(result, indent=4))


def find_most_effective():
    model = NaiveBayesModel(['hamidrasaee', 'MJ_Akbarin'])
    model.load('model_1523953281')

    import json
    print(json.dumps(model.find_must_effecting_words('MJ_Akbarin', 1000), indent=4, ensure_ascii=False))
    print("------------------")
    print(json.dumps(model.find_must_effecting_words('hamidrasaee', 1000), indent=4, ensure_ascii=False))


def extract_words_for_mallet():
    model = NaiveBayesModel(['hamidrasaee', 'MJ_Akbarin'])
    model.load('model_1523953281')

    most_effective = model.find_must_effecting_words('MJ_Akbarin', 40000) + \
                     model.find_must_effecting_words('hamidrasaee', 10000)

    most_effective = list(set([i[0] for i in most_effective]))

    import json
    with open('most_effective_words.json', 'w', encoding='utf8') as f:
        json.dump(most_effective, f, ensure_ascii=False)


def main():
    # train()
    # evaluate()
    # find_most_effective()
    extract_words_for_mallet()


if __name__ == '__main__':
    main()
