#!/usr/bin/env python3

import cv2
import sys
from os.path import exists


def decrypt(img):  # only for greyscale images

    x, y = img.shape[: 2]

    byte = ""
    msg = ""

    k = 0

    for i in range(x):
        for j in range(y):
            byte += str(img[i, j] & 1)
            k += 1
            if (k == 8):
                msg += chr(int(byte, 2))
                k = 0
                byte = ""

    pos = msg.find('_')
    msg_len = int(msg[: pos])

    return msg[pos + 1: pos + 1 + msg_len]


if len(sys.argv) != 2:
    print(f"usage: {sys.argv[0]} <filename>")
    exit(1)

filename = sys.argv[1]

if not exists(filename):
    print("file doesn't exists")
    exit(1)

# converting the image into greyscale
img = cv2.imread(filename)

x, y = img.shape[: 2]

gs_img = cv2.numpy.zeros([x, y], dtype=cv2.numpy.uint8)

for i in range(x):
    for j in range(y):
        gs_img[i, j] = cv2.numpy.mean(img[i, j])

decrypted_msg = decrypt(gs_img.copy())

print(decrypted_msg)
