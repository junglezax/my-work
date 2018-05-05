# plain_to_sub_dir.py
import os
import shutil

from label_util import mk_sub_dirs, old_num2ch


def read_plain(d, dst):
    mk_sub_dirs(dst)

    bmps = os.listdir(d)
    for bmp in bmps:
        if bmp.endswith('.bmp'):
            ss = bmp.split('_')
            if len(ss) < 2:
                print('bad', bmp)
            else:
                lbl = int(ss[0])
                ch = old_num2ch[lbl]
                sub_d = os.path.join(dst, ch)
                src_bmp = os.path.join(d, bmp)
                dst_bmp = os.path.join(sub_d, bmp)
                print('copying', bmp)
                if not os.path.exists(dst_bmp):
                    shutil.copy(src_bmp, dst_bmp)


def main():
    d = '/Users/jiang/data_set/container/container-20160710'
    dst = '/Users/jiang/data_set/container/container-20160710_sub'
    read_plain(d, dst)


if __name__ == '__main__':
    main()
