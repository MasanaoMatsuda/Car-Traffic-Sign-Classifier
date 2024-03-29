import tensorflow as tf
from tensorflow.contrib.layers import flatten

class LeNet5:

    def __architecture__(self):
        # 32x32x3 => 28x28x6 => 14x14x6
        conv1 = tf.nn.conv2d(self.x, self.weights['cw1'], strides=[1,1,1,1], padding='VALID') + self.biases['cb1']
        conv1 = tf.nn.relu(conv1)
        conv1 = tf.nn.max_pool(conv1, ksize=[1,2,2,1], strides=[1,2,2,1], padding='VALID')
        self.conv1 = conv1
        # 14x14x6 => 10x10x16 => 5x5x16
        conv2 = tf.nn.conv2d(conv1, self.weights['cw2'], [1,1,1,1], 'VALID') + self.biases['cb2']
        conv2 = tf.nn.relu(conv2)
        conv2 = tf.nn.max_pool(conv2, [1,2,2,1], [1,2,2,1], 'VALID')
        self.conv2 = conv2
        # 5x5x16 => 1x400
        fc0 = flatten(conv2)
        # 1x400 => 1x120
        fc1 = tf.matmul(fc0, self.weights['fw1']) + self.biases['fb1']
        fc1 = tf.nn.relu(fc1)
        # 1x120 => 1x84
        fc2 = tf.matmul(fc1, self.weights['fw2']) + self.biases['fb2']
        fc2 = tf.nn.relu(fc2)
        # 1x84 => num of classes
        fc3 = tf.matmul(fc2, self.weights['fw3']) + self.biases['fb3']
        return fc3

    def __train__(self):
        cross_entropy = tf.nn.softmax_cross_entropy_with_logits(labels=self._one_hot, logits=self.logits)
        loss = tf.reduce_mean(cross_entropy)
        return self._optimizer.minimize(loss)

    def __evaluate__(self):
        correct_prediction = tf.equal(tf.argmax(self.logits, 1), tf.argmax(self._one_hot, 1))
        return tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    def __init__(self, in_channel, out_classes, optimizer, mu=0, sigma=0.1):
        self.weights = {
            'cw1': tf.Variable(tf.truncated_normal((5,5,in_channel,6), mu, sigma)),
            'cw2': tf.Variable(tf.truncated_normal((5,5,6,16), mu, sigma)),
            'fw1': tf.Variable(tf.truncated_normal((400,120), mu, sigma)),
            'fw2': tf.Variable(tf.truncated_normal((120,84), mu, sigma)),
            'fw3': tf.Variable(tf.truncated_normal((84,out_classes), mu, sigma))
            }
        self.biases = {
            'cb1': tf.Variable(tf.zeros(6)),
            'cb2': tf.Variable(tf.zeros(16)),
            'fb1': tf.Variable(tf.zeros(120)),
            'fb2': tf.Variable(tf.zeros(84)),
            'fb3': tf.Variable(tf.zeros(out_classes))
            }
        self.x = tf.placeholder(tf.float32, shape=(None, 32, 32, in_channel))
        self.y = tf.placeholder(tf.int32, (None))
        self._one_hot = tf.one_hot(self.y, out_classes)
        self._optimizer = optimizer
        self.logits = self.__architecture__()
        self.train = self.__train__()
        self.evaluate = self.__evaluate__()


class LeNet5_deform:

    def __architecture__(self):
        # 32x32x3 => 28x28x10 => 14x14x10
        conv1a = tf.nn.conv2d(self.x, self.weights['cw1a'], strides=[1,1,1,1], padding='VALID') + self.biases['cb1a']
        conv1a = tf.nn.relu(conv1a)
        conv1b = tf.nn.conv2d(conv1a, self.weights['cw1b'], strides=[1,1,1,1], padding='VALID') + self.biases['cb1b']
        conv1b = tf.nn.relu(conv1b)
        conv1 = tf.nn.max_pool(conv1b, ksize=[1,2,2,1], strides=[1,2,2,1], padding='VALID')
        self.conv1a = conv1a
        self.conv1b = conv1b

        # 14x14x10 => 10x10x16 => 5x5x16
        conv2a = tf.nn.conv2d(conv1, self.weights['cw2a'], [1,1,1,1], 'VALID') + self.biases['cb2a']
        conv2a = tf.nn.relu(conv2a)
        conv2b = tf.nn.conv2d(conv2a, self.weights['cw2b'], [1,1,1,1], 'VALID') + self.biases['cb2b']
        conv2b = tf.nn.relu(conv2b)
        conv2 = tf.nn.max_pool(conv2b, [1,2,2,1], [1,2,2,1], 'VALID')
        self.conv2a = conv2a
        self.conv2b = conv2b

        # 5x5x16 => 1x400
        fc0 = flatten(conv2)
        # 1x400 => 1x120
        fc1 = tf.matmul(fc0, self.weights['fw1']) + self.biases['fb1']
        fc1 = tf.nn.relu(fc1)
        # 1x120 => 1x84
        fc2 = tf.matmul(fc1, self.weights['fw2']) + self.biases['fb2']
        fc2 = tf.nn.relu(fc2)
        # 1x84 => num of classes
        fc3 = tf.matmul(fc2, self.weights['fw3']) + self.biases['fb3']
        return fc3

    def __train__(self):
        cross_entropy = tf.nn.softmax_cross_entropy_with_logits(labels=self._one_hot, logits=self.logits)
        loss = tf.reduce_mean(cross_entropy)
        return self._optimizer.minimize(loss)

    def __evaluate__(self):
        correct_prediction = tf.equal(tf.argmax(self.logits, 1), tf.argmax(self._one_hot, 1))
        return tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    def __init__(self, in_channel, out_classes, optimizer, mu=0, sigma=0.1):
        self.weights = {
            'cw1a': tf.Variable(tf.truncated_normal((3,3,in_channel,6), mu, sigma)),
            'cw1b': tf.Variable(tf.truncated_normal((3,3,6,6), mu, sigma)),
            'cw2a': tf.Variable(tf.truncated_normal((3,3,6,16), mu, sigma)),
            'cw2b': tf.Variable(tf.truncated_normal((3,3,16,16), mu, sigma)),
            'fw1': tf.Variable(tf.truncated_normal((400,120), mu, sigma)),
            'fw2': tf.Variable(tf.truncated_normal((120,84), mu, sigma)),
            'fw3': tf.Variable(tf.truncated_normal((84,out_classes), mu, sigma))
            }
        self.biases = {
            'cb1a': tf.Variable(tf.zeros(6)),
            'cb1b': tf.Variable(tf.zeros(6)),
            'cb2a': tf.Variable(tf.zeros(16)),
            'cb2b': tf.Variable(tf.zeros(16)),
            'fb1': tf.Variable(tf.zeros(120)),
            'fb2': tf.Variable(tf.zeros(84)),
            'fb3': tf.Variable(tf.zeros(out_classes))
            }
        self.x = tf.placeholder(tf.float32, shape=(None, 32, 32, in_channel))
        self.y = tf.placeholder(tf.int32, (None))
        self._one_hot = tf.one_hot(self.y, out_classes)
        self._optimizer = optimizer
        self.logits = self.__architecture__()
        self.train = self.__train__()
        self.evaluate = self.__evaluate__()
