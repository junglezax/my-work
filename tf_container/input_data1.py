# test_read_images1.py
import os

import cv2
import numpy as np


def read_data_sets(img_dir):
    lst = []
    labels = []
    for d in os.listdir(img_dir):
        sub_d = os.path.join(img_dir, d)
        if os.path.isdir(sub_d):
            for img in os.listdir(sub_d):
                if img.endswith(".bmp"):
                    img_fn = os.path.join(sub_d, img)
                    # print('reading', img_fn)
                    lst.append(cv2.imread(img_fn).flatten())
                    labels.append(d)
                # else:
                    # print('img not bmp:', img)
    labels = map_labels(labels)
    return np.array(lst), np.array(labels)


def map_labels(labels):
    uniq_labels = sorted(list(set(labels)))
    print('uniq_labels', uniq_labels)
    d = {}
    for idx, ch in enumerate(uniq_labels):
        d[ch] = idx
    print('d', d)
    return [d[ch] for ch in labels]


def main():
    img_dir = '/Users/jiang/data_set/container/cont180430'
    data, labels = read_data_sets(img_dir)
    print('data.shape:', data.shape)
    print('labels.shape:', labels.shape)
    print('labels:', len(labels))

if __name__ == '__main__':
    main()
