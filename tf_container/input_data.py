# test_read_images1.py
import os
from random import shuffle

import cv2
import numpy
from tensorflow.python.framework import dtypes
from tensorflow.contrib.learn.python.learn.datasets import base

from label_util import ch2num

def read_images(img_dir):
    lst = []
    for d in os.listdir(img_dir):
        sub_d = os.path.join(img_dir, d)
        if os.path.isdir(sub_d):
            for img in os.listdir(sub_d):
                if img.endswith(".bmp"):
                    img_fn = os.path.join(sub_d, img)
                    # print('reading', img_fn)
                    # .flatten()
                    lst.append((cv2.imread(img_fn), d))
                    # else:
                    # print('img not bmp:', img)

    shuffle(lst)

    images, labels = zip(*lst)
    labels = map_labels(labels)
    return numpy.array(images), numpy.array(labels)


def map_labels0(labels):
    uniq_labels = sorted(list(set(labels)))
    print('uniq_labels', uniq_labels)
    d = {}
    for idx, ch in enumerate(uniq_labels):
        d[ch] = idx
    print('d', d)
    return [d[ch] for ch in labels]


def map_labels(labels):
    return [ch2num[ch] for ch in labels]


class DataSet(object):
    def __init__(self,
                 images,
                 labels,
                 fake_data=False,
                 one_hot=False,
                 dtype=dtypes.float32,
                 reshape=True):
        """Construct a DataSet.
        one_hot arg is used only if fake_data is true.  `dtype` can be either
        `uint8` to leave the input as `[0, 255]`, or `float32` to rescale into
        `[0, 1]`.
        """
        dtype = dtypes.as_dtype(dtype).base_dtype
        if dtype not in (dtypes.uint8, dtypes.float32):
            raise TypeError('Invalid image dtype %r, expected uint8 or float32' %
                            dtype)
        if fake_data:
            self._num_examples = 10000
            self.one_hot = one_hot
        else:
            assert images.shape[0] == labels.shape[0], (
                'images.shape: %s labels.shape: %s' % (images.shape, labels.shape))
            self._num_examples = images.shape[0]

            # Convert shape from [num examples, rows, columns, depth]
            # to [num examples, rows*columns] (assuming depth == 1)
            if reshape:
                print('images.shape', images.shape)
                # assert images.shape[3] == 1
                images = images.reshape(images.shape[0],
                                        images.shape[1] * images.shape[2] * images.shape[3])
            if dtype == dtypes.float32:
                # Convert from [0, 255] -> [0.0, 1.0].
                images = images.astype(numpy.float32)
                images = numpy.multiply(images, 1.0 / 255.0)

        print('images.shape', images.shape)
        print('labels.shape', labels.shape)

        self._images = images
        self._labels = labels
        self._epochs_completed = 0
        self._index_in_epoch = 0

    @property
    def images(self):
        return self._images

    @property
    def labels(self):
        return self._labels

    @property
    def num_examples(self):
        return self._num_examples

    @property
    def epochs_completed(self):
        return self._epochs_completed

    def next_batch(self, batch_size, fake_data=False):
        """Return the next `batch_size` examples from this data set."""
        if fake_data:
            fake_image = [1] * 784
            if self.one_hot:
                fake_label = [1] + [0] * 9
            else:
                fake_label = 0
            return [fake_image for _ in range(batch_size)], [
                fake_label for _ in range(batch_size)
                ]
        start = self._index_in_epoch
        self._index_in_epoch += batch_size
        if self._index_in_epoch > self._num_examples:
            # Finished epoch
            self._epochs_completed += 1
            # Shuffle the data
            perm = numpy.arange(self._num_examples)
            numpy.random.shuffle(perm)
            self._images = self._images[perm]
            self._labels = self._labels[perm]
            # Start next epoch
            start = 0
            self._index_in_epoch = batch_size
            assert batch_size <= self._num_examples
        end = self._index_in_epoch
        return self._images[start:end], self._labels[start:end]


def read_data_sets(train_dir,
                   fake_data=False,
                   one_hot=False,
                   dtype=dtypes.float32,
                   reshape=True,
                   validation_size=None):
    if fake_data:
        def fake():
            return DataSet([], [], fake_data=True, one_hot=one_hot, dtype=dtype)

        train = fake()
        validation = fake()
        test = fake()
        return base.Datasets(train=train, validation=validation, test=test)

    train_images, train_labels = read_images(train_dir)
    print('train_images.shape', train_images.shape, len(train_images))
    print('train_labels.shape', train_labels.shape)

    if validation_size is None:
        validation_size = int(len(train_images) * 0.3)

    if not 0 <= validation_size <= len(train_images):
        raise ValueError(
            'Validation size should be between 0 and {}. Received: {}.'
                .format(len(train_images), validation_size))

    validation_images = train_images[:validation_size]
    validation_labels = train_labels[:validation_size]
    train_images = train_images[validation_size:]
    train_labels = train_labels[validation_size:]

    train = DataSet(train_images, train_labels, dtype=dtype, reshape=reshape)
    validation = DataSet(validation_images,
                         validation_labels,
                         dtype=dtype,
                         reshape=reshape)
    return base.Datasets(train=train, validation=None, test=validation)


def test_read_images():
    img_dir = '/Users/jiang/data_set/container/cont180430'
    data, labels = read_images(img_dir)
    print('data.shape:', data.shape)
    print('labels.shape:', labels.shape)
    print('labels:', len(labels))


def main():
    img_dir = '/Users/jiang/data_set/container/cont180430'
    data = read_data_sets(img_dir)


if __name__ == '__main__':
    main()
