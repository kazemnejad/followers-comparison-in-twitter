import math
import pickle

import time


class NaiveBayesModel:
    def __init__(self, labels):
        self.labels = labels

        self.vocabulary = set()

        self.words_count = {}
        self.documents_count = {}
        self.total_word_counts_cache = {}
        for l in labels:
            self.words_count[l] = dict()
            self.documents_count[l] = 0
            self.total_word_counts_cache[l] = 0

    def save(self):
        params = {
            'labels': self.labels,
            'vocab': self.vocabulary,
            'words_counts': self.words_count,
            'documents_count': self.documents_count,
            'total_word_counts_cache': self.total_word_counts_cache
        }

        timestamp = str(int(time.time()))
        with open('model_' + timestamp, 'wb') as handle:
            pickle.dump(params, handle, protocol=pickle.HIGHEST_PROTOCOL)

        print('saved in model_%s' % timestamp)

    def load(self, filename):
        with open(filename, 'rb') as handle:
            params = pickle.load(handle)

        self.labels = params['labels']
        self.vocabulary = params['vocab']
        self.words_count = params['words_counts']
        self.documents_count = params['documents_count']
        self.total_word_counts_cache = params['total_word_counts_cache']

    def train(self, iterator):
        """
        :param iterator: iterator of (bag_of_word_list, label)
        """
        for words, label in iterator:
            self.documents_count[label] += 1
            words_count = self.words_count[label]
            for w in words:
                self.vocabulary.add(w)
                words_count[w] = words_count.get(w, 0) + 1

            print("\n...")
            print(self.documents_count)

        for l in self.labels:
            self.total_word_counts_cache[l] = sum(self.words_count[l].values())

    def predict(self, words):
        total_num_docs = sum(self.documents_count.values())

        result = {}
        for label in self.labels:
            words_count = self.words_count[label]

            p_c = math.log(self.documents_count[label] * 1.0 / total_num_docs)
            P = []
            for w in words:
                numerator, denominator = self._add_1_smoothing(
                    words_count.get(w, 0),
                    self.total_word_counts_cache[label]
                )

                P.append(math.log(numerator * 1.0 / denominator))

            result[label] = sum([p_c] + P)

        max_score = result[self.labels[0]]
        best_matching = self.labels[0]
        for label, score in result.items():
            if score > max_score:
                max_score = score
                best_matching = label

        # print(result)

        return best_matching

    def eval(self, eval_set_iterator):
        confusion_matrix = {'fn': 0, 'tn': 0, 'fp': 0, 'tp': 0}

        result = {}
        for label in self.labels:
            result[label] = confusion_matrix.copy()

        count = 0
        for words, data_label in eval_set_iterator:
            for label in self.labels:
                table = result[label]

                prediction = self.predict(words)

                if label == data_label:
                    if prediction == label:
                        table['tp'] += 1
                    else:
                        table['fn'] += 1
                else:
                    if prediction != label:
                        table['tn'] += 1
                    else:
                        table['fp'] += 1

            count += 1
            print('# %s' % count)

        final_result = {}
        for label, table in result.items():
            precision = table['tp'] * 1.0 / (table['tp'] + table['fp'])
            recall = table['tp'] * 1.0 / (table['tp'] + table['fn'])
            final_result[label] = {
                'precision': precision * 100,
                'recall': recall * 100,
                'accuracy': (table['tp'] + table['tn']) * 1.0 / (table['tp'] + table['tn'] + table['fp'] + table['fn']),
                'f1': 2.0 * (precision * recall) / (precision + recall)
            }

        return final_result

    def find_must_effecting_words(self, label, k):
        probs = []
        for w in self.vocabulary:
            diffs = []
            for other_label in self.labels:
                if other_label == label:
                    continue

                diffs.append(self._calculate_prob(label, w) - self._calculate_prob(other_label, w))

            probs.append((w, sum(diffs)))

        probs.sort(key=lambda x: x[1], reverse=True)
        return probs[:k]

    def _calculate_prob(self, label, word):
        words_count = self.words_count[label]
        numerator, denominator = self._add_1_smoothing(
            words_count.get(word, 0),
            self.total_word_counts_cache[label]
        )

        return math.log(numerator * 1.0 / denominator)

    def _add_1_smoothing(self, w_c, total):
        return (w_c + 1), (total + len(self.vocabulary) + 1)
