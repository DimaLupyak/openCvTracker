# pylint: disable=no-member
import cv2
import sys
from random import randint

W = 600
H = 400

def track(video, bboxes):
    colors = []
    multiTracker = cv2.MultiTracker_create()
    video = cv2.VideoCapture(video)
    ok, frame = video.read()
    if not ok: 
        return
    resized_frame = cv2.resize(frame, (W, H))
    for bbox in bboxes:
        try: 
            multiTracker.add(cv2.TrackerMedianFlow_create(), resized_frame, bbox)
            colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
        except: pass
    while video.isOpened():    
        ok, frame = video.read()        
        if not ok: 
            continue
        resized_frame = cv2.resize(frame, (W, H))
        ok, bboxes = multiTracker.update(resized_frame)
        if not ok: 
            continue
        for i, newbox in enumerate(bboxes):
            p1 = (int(newbox[0]), int(newbox[1]))
            p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
            cv2.rectangle(resized_frame, p1, p2, colors[i], 2, 1)        
        cv2.imshow("Title", resized_frame)
        input_key = cv2.waitKey(1)      
        if input_key == 27: 
            break # Exit if ESC pressed
        if input_key & 0xFF == ord('a'): # a - add new box
            try:
                rand_x = randint(50, W - 50)
                rand_y = randint(50, H - 50)
                multiTracker.add(cv2.TrackerMedianFlow_create(), resized_frame, (rand_x, rand_y, 40, 40))
                colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
            except: pass
        if input_key & 0xFF == ord('d'): # a - add new box
            try:
                multiTracker.)
                colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
            except: pass
    cv2.destroyAllWindows()

def main():
    input_video ='rtsp://Oleksii:eLtGk4Cb@31.42.173.15:8072'
    bboxes = []    
    video = cv2.VideoCapture(input_video)
    ok, frame = video.read()
    if not ok: 
        return
    resized_frame = cv2.resize(frame, (W, H)) 
    while True:
        bbox = cv2.selectROI('MultiTracker', resized_frame)
        bboxes.append(bbox)        
        print("Press q to quit selecting boxes and start tracking")
        print("Press any other key to select next object")
        if ((cv2.waitKey(0) & 0xFF) == 113):  # q is pressed
            break      
    print('Selected bounding boxes {}'.format(bboxes))
    track(input_video, bboxes)

if __name__ == '__main__':
    main()