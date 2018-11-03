# pylint: disable=no-member
# pylint: disable-msg=too-many-arguments
import cv2
import sys
from random import randint

class cars_tracker:
    video_url: str
    bboxes = []
    colors = []
    frame_weight = 600
    frame_height = 400
    def __init__(self, video_url: str):
        self.video_url = video_url
        self.multiTracker = cv2.MultiTracker_create()
        self.video = cv2.VideoCapture(self.video_url)

    def add_car(self):
        ok, frame = self.video.read()
        if not ok:
            return
        resized_frame = cv2.resize(frame, (self.frame_weight, self.frame_height))
        try:
            rand_x = randint(50, self.frame_weight - 50)
            rand_y = randint(50, self.frame_height - 50)
            bbox = (rand_x, rand_y, 40, 40)
            self.bboxes.append(bbox)
            self.colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
            self.multiTracker.add(cv2.TrackerMedianFlow_create(), resized_frame, bbox)            
        except: pass

    def update(self):  
        ok, frame = self.video.read()        
        if not ok: 
            return
        resized_frame = cv2.resize(frame, (self.frame_weight, self.frame_height))
        ok, new_bboxes = self.multiTracker.update(resized_frame)
        if not ok: 
            return
        for i, newbox in enumerate(new_bboxes):
            p1 = (int(newbox[0]), int(newbox[1]))
            p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
            cv2.rectangle(resized_frame, p1, p2, self.colors[i], 2, 1)        
        cv2.imshow("Title", resized_frame)
        

def main():
    video_url ='rtsp://Oleksii:eLtGk4Cb@31.42.173.15:8072'
    tracker = cars_tracker(video_url)
    while tracker.video.isOpened():
        tracker.update()
        input_key = cv2.waitKey(1)
        if input_key == 27: 
            break # Exit if ESC pressed        
        if input_key & 0xFF == ord('a'): # a - add new box
            try:
                tracker.add_car()
            except: pass
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()