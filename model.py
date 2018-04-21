#
# Created by amirhosein on 20/27/18.
#

from datetime import datetime

import tensorflow as tf
import numpy as np
from tensorflow.python.keras._impl.keras.utils import Progbar

from utils import one_hot, minibatches


class Config:
    max_document_length = 40
    embedding_size = 200
    filter_sizes = [2, 3, 4]
    num_filters = 128
    num_classes = 2
    vocabulary_size = 1000002
    padding = 'valid'
    dropout_keep = 0.6
    learning_rate = 0.005
    num_epoch = 10
    batch_size = 512
    use_static = False

    def __init__(self, output_path=None):
        if output_path:
            # Where to save things.
            self.output_path = output_path
        else:
            self.output_path = "results/{:%Y%m%d_%H%M%S}/".format(datetime.now())
        self.model_output = self.output_path + "model.weights"
        self.eval_output = self.output_path + "results.txt"
        self.log_output = self.output_path + "log"


class SingleCNNText:
    NULL_ID = 0
    UNKNOWN_ID = 0

    def __init__(self, config, embeddings=None, word_to_id=None, vocab=None):
        self.config = config
        self._word_to_id = word_to_id
        self._vocab = vocab

        if config.use_static:
            self._create_pretrained_embedding(embeddings)
            self.config.vocabulary_size = self.pretrained_embeddings.shape[0]
            print(self.config.vocabulary_size)

        self._build()

    def add_placeholders(self):
        self.input_placeholder = tf.placeholder(tf.int32, [None, self.config.max_document_length], 'input')
        self.label_placeholder = tf.placeholder(tf.int32, [None, self.config.num_classes], 'labels')
        self.dropout_keep_placeholder = tf.placeholder(tf.float32, name='dropout_keep')

    def create_feed_dict(self, batch_input, batch_labels=None, dropout_keep=1.0):
        feed = {
            self.input_placeholder: batch_input,
            self.dropout_keep_placeholder: dropout_keep,
        }

        if batch_labels is not None:
            feed[self.label_placeholder] = batch_labels

        return feed

    def add_embeddings(self):
        if self.config.use_static:
            pretrained = tf.constant(self.pretrained_embeddings)
        else:
            pretrained = tf.Variable(tf.random_uniform(
                [self.config.vocabulary_size, self.config.embedding_size],
                -1.0,
                1.0)
            )

        embeddings = tf.nn.embedding_lookup(pretrained, self.input_placeholder)
        embeddings = tf.expand_dims(embeddings, -1)

        return embeddings

    def add_convolutions(self):
        x = self.add_embeddings()

        convs = []
        for filter_size in self.config.filter_sizes:
            filter_shape = (filter_size, self.config.embedding_size)
            conv = tf.layers.conv2d(
                inputs=x,
                filters=self.config.num_filters,
                kernel_size=filter_shape,
                strides=(1, 1),
                padding=self.config.padding,
                activation=tf.nn.relu,
                name='conv2d-%s' % filter_size
            )

            convs.append(conv)

        return convs

    def add_pooling(self):
        convs = self.add_convolutions()

        max_pools = []
        for conv in convs:
            pool_shape = (conv.shape[1], 1)
            mp = tf.layers.max_pooling2d(
                inputs=conv,
                pool_size=pool_shape,
                strides=(1, 1),
                padding=self.config.padding
            )

            max_pools.append(mp)

        return max_pools

    def add_pooling_flatten(self):
        pools = self.add_pooling()

        num_total_features = len(self.config.filter_sizes) * self.config.num_filters
        flatten = tf.reshape(
            tf.concat(pools, 3),
            [-1, num_total_features]
        )

        return flatten

    def add_logits_ops(self):
        x = self.add_pooling_flatten()
        x_drop = tf.nn.dropout(x, self.dropout_keep_placeholder)

        num_total_features = len(self.config.filter_sizes) * self.config.num_filters
        W = tf.get_variable(
            'W',
            shape=[num_total_features, self.config.num_classes],
            initializer=tf.contrib.layers.xavier_initializer()
        )
        b = tf.zeros([self.config.num_classes], dtype=tf.float32, name='b')

        logits = tf.nn.xw_plus_b(x_drop, W, b, name='logits')

        return logits

    def add_predict_ops(self, logits):
        return tf.argmax(logits, 1, name='predict')

    def add_accuracy_ops(self, predictions):
        correct = tf.equal(predictions, tf.argmax(self.input_placeholder, 1))
        return tf.reduce_mean(tf.cast(correct, 'float'), name='accuracy')

    def add_loss_ops(self, logits):
        return tf.reduce_mean(
            tf.nn.softmax_cross_entropy_with_logits_v2(logits=logits, labels=self.label_placeholder)
            , name='loss')

    def add_training_ops(self, loss):
        return tf.train.AdamOptimizer(self.config.learning_rate).minimize(loss, name='train')

    def _build(self):
        self.add_placeholders()

        logits = self.add_logits_ops()
        self.predict = self.add_predict_ops(logits)
        self.loss = self.add_loss_ops(logits)
        self.accuracy = self.add_accuracy_ops(self.predict)

        self.train = self.add_training_ops(self.loss)

    def train_on_batch(self, sess, inputs_batch, labels_batch):
        feed = self.create_feed_dict(inputs_batch, labels_batch, self.config.dropout_keep)
        _, loss, accuracy = sess.run([self.train, self.loss, self.accuracy], feed_dict=feed)
        return loss, accuracy

    def predict_on_batch(self, sess, input_batch):
        feed = self.create_feed_dict(input_batch)
        predictions = sess.run([self.predict], feed)
        return predictions[0]

    def fit(self, session, saver, train_set_raw, dev_set_raw):
        print('start pre processing data...')
        train_set = self.pre_process_data(train_set_raw)
        print('done pre processing data!')
        dev_set = self.pre_process_data(dev_set_raw, False)

        for epoch in range(self.config.num_epoch):
            print('Epoch %d / %d\n' % (epoch + 1, self.config.num_epoch))

            prog_bar = Progbar(1 + int(len(train_set) / self.config.batch_size))

            for i, (input_batch, label_batch) in enumerate(minibatches(train_set, self.config.batch_size)):
                loss, accuracy = self.train_on_batch(session, input_batch, label_batch)
                prog_bar.update(i, [('loss', loss), ('accuracy', accuracy)])

            saver.save(session, self.config.model_output)

            result = self.evaluate(session, None, dev_set)
            import json
            print(json.dumps(result))

    def output(self, sess, inputs=None):
        prog = Progbar(1 + int(len(inputs) / self.config.batch_size))

        preds = np.empty((0, 2))
        for i, (input_batch, label_batch) in enumerate(minibatches(inputs, self.config.batch_size, shuffle=False)):
            prediction_batch = self.predict_on_batch(sess, input_batch)
            evaluation_batch = np.concatenate([
                prediction_batch.reshape((-1, 1)),
                label_batch.reshape((-1, 1))
            ], axis=1)

            preds = np.concatenate([preds, evaluation_batch])

            prog.update(i + 1, [])

        return preds

    def evaluate(self, session, dev_set_raw, dev_set=None):
        print("\nEval on dev set\n")
        if dev_set is None:
            dev_set = self.pre_process_data(dev_set_raw, False)

        confusion_matrix = {'fn': 0, 'tn': 0, 'fp': 0, 'tp': 0}

        result = [None] * self.config.num_classes
        for label in range(self.config.num_classes):
            result[label] = confusion_matrix.copy()

        count = 0
        model_output = self.output(session, dev_set)
        for prediction, actual_label in model_output:
            for label in range(self.config.num_classes):
                table = result[label]

                if label == actual_label:
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
        for label, table in enumerate(result):
            precision = table['tp'] * 1.0 / (table['tp'] + table['fp'])
            recall = table['tp'] * 1.0 / (table['tp'] + table['fn'])
            final_result[label] = {
                'precision': precision * 100,
                'recall': recall * 100,
                'accuracy': (table['tp'] + table['tn']) * 1.0 / (table['tp'] + table['tn'] + table['fp'] + table['fn']),
                'f1': 2.0 * (precision * recall) / (precision + recall)
            }

        return final_result

    def pre_process_data(self, data, convert_to_one_hot=True):
        '''
        :param data: [ ([token1, token2, ..., tokenN], label_id) , ... ]
        :return: [ ([token_id1, token_id2, ..., token_idN], one_hot(label)), ... ]
        '''
        if not self.config.use_static:
            return self.pre_process_data_from_vocab(data, convert_to_one_hot)

        max_length = self.config.max_document_length

        i = 0
        final_data = []
        for document, label in data:
            doc_word_ids = [self._word_to_id.get(token, self.UNKNOWN_ID) for token in document]
            doc_word_ids += [self.NULL_ID] * (max_length - len(document))

            if convert_to_one_hot:
                o_label = one_hot(self.config.num_classes, label)
            else:
                o_label = label

            final_data.append((np.array(doc_word_ids[:max_length]), o_label))

            i += 1
            print("#", i)

        return final_data

    def pre_process_data_from_vocab(self, data, convert_to_one_hot=True):
        '''
        :param data: [ ([token1, token2, ..., tokenN], label_id) , ... ]
        :return: [ ([token_id1, token_id2, ..., token_idN], one_hot(label)), ... ]
        '''
        max_length = self.config.max_document_length

        null_id = self._vocab['<NULL>']
        unk_id = self._vocab['<UNK>']

        i = 0
        final_data = []
        for document, label in data:
            doc_word_ids = [self._vocab.get(token, unk_id) for token in document]
            doc_word_ids += [null_id] * (max_length - len(document))

            if convert_to_one_hot:
                o_label = one_hot(self.config.num_classes, label)
            else:
                o_label = label

            final_data.append((np.array(doc_word_ids[:max_length]), o_label))

            i += 1
            print("#", i)

        return np.array(final_data)

    def _create_pretrained_embedding(self, embeddings):
        defaults = np.array([
            np.full([self.config.embedding_size], 0, dtype=np.float32),
            np.full([self.config.embedding_size], -0.037, dtype=np.float32),
        ])

        self.pretrained_embeddings = np.concatenate([embeddings, defaults])

        assert self.pretrained_embeddings.shape[0] - 1 not in self._word_to_id
        assert self.pretrained_embeddings.shape[0] - 2 not in self._word_to_id

        self.UNKNOWN_ID = self.pretrained_embeddings.shape[0] - 1
        self.NULL_ID = self.pretrained_embeddings.shape[0] - 2
