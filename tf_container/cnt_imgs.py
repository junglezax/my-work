# cnt_imgs.py
import os


def cnt_imgs(img_dir):
    cnts = {}
    for d in os.listdir(img_dir):
        sub_d = os.path.join(img_dir, d)
        if os.path.isdir(sub_d):
            cnt = 0
            for img in os.listdir(sub_d):
                if img.endswith(".bmp"):
                    cnt += 1
            cnts[d] = cnt
            print(d, cnt)
    total = sum([v for k, v in cnts.items()])
    total_char = total - cnts['non_char']
    print('cnts:', cnts)
    print('total:', total)
    print('total char:', total_char)
    print('non_char:', cnts['non_char'])
    print('non_char/char:', cnts['non_char']/float(total_char))  # 1.7


if __name__ == '__main__':
    cnt_imgs('/Users/jiang/data_set/container/container-20160710_sub')