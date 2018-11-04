# pylint: disable=no-member
# pylint: disable-msg=too-many-arguments
import cv2
import sys
from models import car_model
from random import randint

class cars_tracker:
    video_url: str
    trackers = []
    frame_weight = 600
    frame_height = 400
    def __init__(self, video_url: str):
        self.video_url = video_url
        self.video = cv2.VideoCapture(self.video_url)

    def add_car(self, box):
        ok, frame = self.video.read()
        if not ok:
            return
        resized_frame = cv2.resize(frame, (self.frame_weight, self.frame_height))
        try:    
            car = car_model(box)
            tracker = cv2.TrackerMedianFlow_create()
            ok = tracker.init(resized_frame, car.box)
            if not ok:
                return
            self.trackers.append((car, tracker))          
        except: pass

    def remove_car(self):
        try:    
            del self.trackers[0]
        except: pass

    def update(self):  
        ok, frame = self.video.read()        
        if not ok: 
            return
        resized_frame = cv2.resize(frame, (self.frame_weight, self.frame_height))
        for tracker in self.trackers:
            ok, newbox = tracker[1].update(resized_frame)
            if not ok: 
                continue
            tracker[0].update_box(newbox)
            p1 = (int(newbox[0]), int(newbox[1]))
            p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
            cv2.rectangle(resized_frame, p1, p2, tracker[0].color, 2, 1)
            for point in tracker[0].box_history:
                p1 = (int(point[0] + point[2] / 2), 
                      int(point[1] + point[3] / 2))
                p2 = (int(point[0] + point[2] / 2 + 1), 
                      int(point[1] + point[3] / 2 + 1))
                cv2.rectangle(resized_frame, p1, p2, tracker[0].color, 2, 1)
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
                rand_x = randint(50, tracker.frame_weight - 50)
                rand_y = randint(50, tracker.frame_height - 50)
                box = (rand_x, rand_y, 40, 40)
                tracker.add_car(box)
            except: pass
        if input_key & 0xFF == ord('d'): # a - add new box
            try:
                tracker.remove_car()
            except: pass
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()