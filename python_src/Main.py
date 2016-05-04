import cv2, CVHelper, put_data
import numpy as np

vc = cv2.VideoCapture(0)
#vc = cv2.VideoCapture('example_2.mp4')

if vc.isOpened():
    print "vc is open!!"
    return_value, frame = vc.read()

while True:
    start = CVHelper.wait_for_color(vc)
    print(start)
    if start != None:
        CVHelper.fill_level(vc, start, put_data.update)
