import cv2, time
import numpy as np

ROI_RECT = [50,50,300,500]
COLOR = 109


def fill_level(feed, start, update_func):
    h_range = 30
    key = -1
    v_thresh = 90
    back = None
    min_area = 100
    fill = start
    window = [fill for i in range(10)]
    update_fill = 0
    frame_num = 0

    while key != 27 and feed.isOpened():
        return_value, frame = feed.read()

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
                    if diff < 150 and diff > 0:
                        window.pop(0)
                        window.append(new_fill)


                cv2.line(current, (0, fill+50), (300, fill+50) ,(0,255,0), 2)

                cv2.putText(current, str(fill/5), (80,100), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)

                update_fill = abs(100 - fill/5)/100.0
                #print(update_fill)
                if (frame_num % 10) == 0:
                    update_func(update_fill)
                delta = current

                if(update_fill > .90):
                    return
            else:
                delta = raw

            cv2.imshow("Main", delta)

            frame_num += 1

        if frame_num == 10:
            back = raw

        key = cv2.waitKey(10)
        if key == ord('q'):
            return


def wait_for_color(feed):
    h_range = 30
    key = -1
    v_range = [15000, 20000]
    frame_count = 0

    while key != 27 and feed.isOpened():
        return_value, frame = feed.read()

        if frame is not None:
            height, width, depth = frame.shape

            full = cv2.pyrDown(frame)
            full = cv2.flip(full, 1)
            frame = full[ROI_RECT[0]:ROI_RECT[0]+ROI_RECT[3] , ROI_RECT[1]:ROI_RECT[1]+ROI_RECT[2]]

            hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv_img)

            h = cv2.inRange(h, COLOR, COLOR+10)
            h_binary = h.copy()
            _, contours, hierarchy = cv2.findContours(h_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            rect = (0,0,0,0)
            if contours is not None and len(contours) > 0:
                l = max(contours, key=lambda cnt: cv2.contourArea(cnt))
                rect = cv2.boundingRect(l)
                area = cv2.contourArea(l)
                if area > v_range[0] and area < v_range[1] and abs(rect[0] - rect[2]) < 1000 and abs(rect[1] - rect[3]) < 1000:
                    frame_count += 1
                    cv2.rectangle(frame, (rect[0], rect[1]), (rect[0]+rect[2],rect[1]+rect[3]), (0,255,0), 2)
                    cv2.putText(frame, str(area), (rect[0],rect[1]), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
                    if frame_count > 50:
                        return 400
                else:
                    frame_count = 0
                    #time.sleep(.5)
            else:
                #time.sleep(.5)
                pass


                #cv2.rectangle(frame, (rect[0], rect[1]), (rect[0]+rect[2],rect[1]+rect[3]), (0,255,0), 2)
                #cv2.putText(frame, str(area), (rect[0],rect[1]), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)

        cv2.imshow("Main", frame)

        key = cv2.waitKey(10)
        if key == ord('q'):
            #return None
            pass

    #return None
