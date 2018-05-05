# extract_char_bmps.py
from __future__ import print_function

import os
import shutil


class CharBmpsExtractor(object):
    def __init__(self, src_dir, dst_dir):
        self.src_dir = src_dir  # '/Users/jiang/data_set/container/1/m95'
        self.dst_dir = dst_dir  # '/Users/jiang/data_set/container/1/cont180430'
        self.data = []
        self.already_exists_cnt = 0
        self.not_exist_bmp_dir = set()

    def extract_char_bmps(self):
        sub_dirs = os.listdir(self.src_dir)
        for sub_dir in sub_dirs:
            sub_d = os.path.join(self.src_dir, sub_dir)
            if os.path.isdir(sub_d):
                # print('sub_d', sub_d)
                self.extract_char_bmps_from_one_dir(sub_d, sub_dir)
                # break

    def extract_char_bmps_from_one_dir(self, sub_d, sub_dir):
        # print('sub_d', sub_d)
        linesr_d = os.path.join(sub_d, 'linesr')
        if not os.path.exists(linesr_d):
            print(linesr_d, 'not exists')
            return

        txts = os.listdir(linesr_d)
        for txt_fn in txts:
            txt = os.path.join(linesr_d, txt_fn)
            # print('txt', txt)
            self.extract_char_bmps_from_one_txt(txt, sub_dir)

    def extract_char_bmps_from_one_txt(self, txt, sub_dir):
        with open(txt) as f:
            for l in f:
                self.extract_one_line(l, sub_dir)

    def extract_one_line(self, line, sub_dir):
        ss = line.split()
        # idx = ss[0]
        bmp_fn = ss[1]
        ch = ss[2]
        # yield bmp_fn, ch
        self.data.append((sub_dir + '__' + bmp_fn, ch))
        # yield bmp_fn, ch

    def merge_data(self):
        dic = {}
        for bmp_fn, ch in self.data:
            if bmp_fn in dic:
                if ch != dic[bmp_fn]:
                    print('conflict:', bmp_fn, ch, dic[bmp_fn])
            else:
                dic[bmp_fn] = ch
        # print(len(dic))

        dic_ch = {}
        for bmp_fn, ch in dic.items():
            if ch in dic_ch:
                dic_ch[ch].append(bmp_fn)
            else:
                dic_ch[ch] = [bmp_fn]

        # print('dir_ch len', len(dic_ch), 'dic_ch cnt', [(k, len(v)) for k, v in dic_ch.items()])
        return dic_ch

    def cp_files(self, merged_data):
        for ch, bmp_fns in merged_data.items():
            dst_dir_ch = os.path.join(self.dst_dir, ch if ch != '[' else 'non_char')
            if not os.path.exists(dst_dir_ch):
                os.mkdir(dst_dir_ch)

            for bmp_fn in bmp_fns:
                # print(bmp_fn)
                dir_name, bmp_name = bmp_fn.split('__')
                bmp_dir = os.path.join(self.src_dir, dir_name, 'bmps')
                if os.path.exists(bmp_dir):
                    bmp_filename = os.path.join(bmp_dir, bmp_name)
                    # print(bmp_filename)

                    dst_filename = os.path.join(dst_dir_ch, bmp_fn)
                    if not os.path.exists(dst_filename):
                        shutil.copy(bmp_filename, dst_filename)
                    else:
                        self.already_exists_cnt += 1
                else:
                    self.not_exist_bmp_dir.add(bmp_dir)

    def do_extract_char_bmps(self):
        self.extract_char_bmps()
        # print(len(self.data))

        merged_data = self.merge_data()
        self.cp_files(merged_data)

        for j in self.not_exist_bmp_dir:
            print(j + ' not exists')

        print('already_exists_cnt', self.already_exists_cnt)


def get_root_dir_from_linesr_dir(linesr_dir):
    ss = linesr_dir.split('/')
    """if len(ss) != 4:
        print('too long:', linesr_dir)
        print(ss[1])"""

    s = '/home/jiang/images/' + '/'.join(ss[1:-2])
    return s


def main():
    linesrs_txt = '/home/jiang/images/linesrs.txt'
    dst_dir = '/home/jiang/images/cntr180505'
    root_dirs = set()
    idx = 0
    with open(linesrs_txt) as f:
        for l in f:
            l = l.strip()
            root_dir = get_root_dir_from_linesr_dir(l)
            # print('%d got root_dir:' % idx, root_dir)
            idx += 1
            root_dirs.add(root_dir)

    print('len root_dirs', len(root_dirs))
    for root_dir in root_dirs:
        print('root_dir:', root_dir)

        e = CharBmpsExtractor(root_dir, dst_dir)
        e.do_extract_char_bmps()
    print('all done')

if __name__ == '__main__':
    main()
