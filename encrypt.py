#!/usr/bin/env python3

import cv2
import sys
from os.path import exists


def encrypt(img, msg):  # only for greyscale images

    x, y = img.shape[: 2]

    l = 0
    byte_stream = ""

    for i in msg:
        byte = bin(ord(i) & 255)[2:]
        byte = (8 - len(byte)) * "0" + byte
        byte_stream += byte

    for i in range(x):
        for j in range(y):
            if byte_stream[l] == '0':
                img[i, j] &= 254
            else:
                img[i, j] |= 1

            l += 1
            if l >= len(byte_stream):
                return img

    return img


if len(sys.argv) != 3:
    print(f"usage: {sys.argv[0]} <filename> <message>")
    exit(1)

filename = sys.argv[1]
msg = sys.argv[2]

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

new_img = encrypt(gs_img.copy(), str(len(msg)) +
                  "_" + msg)  # message overlayed

# new_name = filename[: filename.rfind('.')] + "_encrypted" + filename[filename.rfind('.'):]
new_name = filename[: filename.rfind('.')] + "_encrypted" + ".png"

cv2.imwrite(new_name, new_img)  # save the new image
