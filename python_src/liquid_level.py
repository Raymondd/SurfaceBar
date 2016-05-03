import cv2
import numpy as np
import server_example as fb

#vc = cv2.VideoCapture(0)

vc = cv2.VideoCapture('example.mp4')

if vc.isOpened():
    print "vc is open!!"
    return_value, frame = vc.read()

h_range = 30
key = -1
v_thresh = 90
ROI_RECT = [50,50,300,500]
back = None
min_area = 100
fill = 500
window = [fill for i in range(10)]
update_fill = 0
frame_num = 0

while key != 27 and vc.isOpened():
    return_value, frame = vc.read()

    if frame is not None:
        height, width, depth = frame.shape

        full = cv2.pyrDown(frame)
        full = cv2.flip(full, 1)
        raw = full[ROI_RECT[0]:ROI_RECT[0]+ROI_RECT[3] , ROI_RECT[1]:ROI_RECT[1]+ROI_RECT[2]]
        current = raw.copy()

        if back != None:
            frameDelta = cv2.absdiff(raw, back)
            thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)

            gray = cv2.cvtColor(thresh,cv2.COLOR_BGR2GRAY)
            ret,thresh = cv2.threshold(gray,127,255,0)
            im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            #cv2.drawContours(current, contours, -1, (0,255,0), 3)
            if contours is not None and len(contours) > 0:
                widest = max(contours, key = lambda x: cv2.boundingRect(x)[3])
                '''for cnt in contours:
                    area = cv2.contourArea(cnt)
                    rect = cv2.boundingRect(cnt)
                    cv2.rectangle(current, (rect[0], rect[1]), (rect[0]+rect[2],rect[1]+rect[3]), (255,0,0), 2)'''

                rect = cv2.boundingRect(widest)
                fill = (sum(window)/len(window))
                new_fill = rect[1]

                diff = fill - new_fill
                if diff < 150 and diff > -50:
                    window.pop(0)
                    window.append(new_fill)

                cv2.line(current, (0, fill+50), (300, fill+50) ,(0,255,0), 2)

            cv2.putText(current, str(fill/5), (80,100), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)

            update_fill = abs(100 - fill/5)/100.0
            #print(update_fill)
            #if (frame_num % 10) == 0:
            #    fb.update(update_fill)
            delta = current
        else:
            delta = raw


        #cv2.imshow("WebCam", full)
        cv2.imshow("Delta", delta)
        #cv2.imshow("Canny", edges)
        #back = raw

        frame_num += 1

    if frame_num == 10:
        back = raw

    key = cv2.waitKey(10)
    if key == ord('q'):
        back = raw
