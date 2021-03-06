# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""A very simple MNIST classifier.
See extensive documentation at
https://www.tensorflow.org/get_started/mnist/beginners
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys

import tensorflow as tf

import input_data

FLAGS = None


def main(_):
    # Import data
    data = input_data.read_data_sets(FLAGS.data_dir)

    # Create the model
    x = tf.placeholder(tf.float32, [None, 12600])
    W = tf.Variable(tf.zeros([12600, 34]))
    b = tf.Variable(tf.zeros([34]))
    y = tf.matmul(x, W) + b

    # Define loss and optimizer
    y_ = tf.placeholder(tf.int64, [None])

    # The raw formulation of cross-entropy,
    #
    #   tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(tf.nn.softmax(y)),
    #                                 reduction_indices=[1]))
    #
    # can be numerically unstable.
    #
    # So here we use tf.losses.sparse_softmax_cross_entropy on the raw
    # outputs of 'y', and then average across the batch.
    cross_entropy = tf.losses.sparse_softmax_cross_entropy(labels=y_, logits=y)
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

    sess = tf.InteractiveSession()
    tf.global_variables_initializer().run()
    # Train
    for _ in range(1000):
        batch_xs, batch_ys = data.train.next_batch(100)
        # print('batch_xs.shape', batch_xs.shape)
        # print('batch_ys.shape', batch_ys.shape)
        sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

    # Test trained model
    correct_prediction = tf.equal(tf.argmax(y, 1), y_)
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    print('data.test.images.shape', data.test.images.shape)
    print('data.test.labels.shape', data.test.labels.shape)
    print(sess.run(
        accuracy, feed_dict={
            x: data.test.images,
            y_: data.test.labels
        }))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--data_dir',
        type=str,
        default='/Users/jiang/data_set/container/cont180430',
        help='Directory for storing input data')
    FLAGS, unparsed = parser.parse_known_args()
    tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
