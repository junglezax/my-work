# label_util.py
import os

ch2num = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'J': 18, 'K': 19, 'L': 20, 'M': 21, 'N': 22, 'P': 23, 'R': 24, 'S': 25, 'T': 26, 'U': 27, 'V': 28, 'W': 29, 'X': 30, 'Y': 31, 'Z': 32, 'non_char': 33}
num2ch = dict([v, k] for k, v in ch2num.items())
# print('num2ch', num2ch)

old_num2ch = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F', 16: 'G', 17: 'H', 18: 'I', 19: 'J', 20: 'K', 21: 'L', 22: 'M', 23: 'N', 24: 'O', 25: 'P', 26: 'Q', 27: 'R', 28: 'S', 29: 'T', 30: 'U', 31: 'V', 32: 'W', 33: 'X', 34: 'Y', 35: 'Z', 36: 'non_char'}
old_ch2num = dict([v, k] for k, v in old_num2ch.items())


def gen_old_num2ch():
    old_num2ch_dict = {}
    for d in range(10):
        ch = chr(ord('0') + d)
        # print(d, ch)
        old_num2ch_dict[d] = ch

    for d in range(10, 36):
        ch = chr(ord('A') + d - 10)
        # print(d, ch)
        old_num2ch_dict[d] = ch

    old_num2ch_dict[36] = 'non_char'
    print(old_num2ch_dict)


def mk_sub_dirs(root_d):
    for ch in ch2num.keys():
        sub_d =  os.path.join(root_d, ch)
        if not os.path.exists(sub_d):
            os.makedirs(sub_d)


if __name__ == '__main__':
    gen_old_num2ch()
