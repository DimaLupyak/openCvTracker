# pylint: disable=no-member
# pylint: disable-msg=too-many-arguments
import cv2
import sys
from models import car_model
from random import randint
import time

class cars_tracker:
    video_url: str
    car_trackers = []
    frame_weight = 600
    frame_height = 400
    left_speeds = []
    right_speeds = []
    last_left_speed = 0
    last_right_speed = 0
    left_gate_start = (250,90,60,5)
    left_gate_finish = (70,190,100,5)
    right_gate_start = (300,260,140,5)
    right_gate_finish = (380,100,90,5)
    left_len = 0.07
    right_len = 0.07
    def __init__(self, video_url: str):
        self.video_url = video_url
        self.video = cv2.VideoCapture(self.video_url)
        self.update()
        cv2.setMouseCallback("Title", self.click_event, self)

    def click_event(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            param.add_car((x-20, y-20, 30, 30), "L")
        if event == cv2.EVENT_RBUTTONDOWN:
            param.add_car((x-20, y-20, 50, 50), "R")

    def add_car(self, box, direction):
        ok, frame = self.video.read()
        if not ok:
            return
        resized_frame = cv2.resize(frame, (self.frame_weight, self.frame_height))
        try:    
            car = car_model(box, direction)
            tracker = cv2.TrackerMedianFlow_create()
            ok = tracker.init(resized_frame, car.init_box)
            if not ok:
                return
            self.car_trackers.append((car, tracker))          
        except: pass

    def remove_car(self):
        try:    
            del self.car_trackers[0]
        except: pass
        
    
    def remove_near_car(self, box):
        try:  
            for i, car_tracker in enumerate(self.car_trackers):
                if have_intersection(car_tracker[0].current_box, box):
                    del self.car_trackers[i]
        except: pass

    def update(self):  
        ok, frame = self.video.read()        
        if not ok: 
            return
        resized_frame = cv2.resize(frame, (self.frame_weight, self.frame_height))
                
        gates = [
            (self.left_gate_start, (255,0,0)), 
            (self.left_gate_finish, (0,0,255)),  
            (self.right_gate_start, (255,0,0)),  
            (self.right_gate_finish, (0,0,255)), 
            ]

        for gate in gates:
            p1 = (int(gate[0][0]), int(gate[0][1]))
            p2 = (int(gate[0][0] + gate[0][2]), int(gate[0][1] + gate[0][3]))
            cv2.rectangle(resized_frame, p1, p2, gate[1], 1, 1)

        
        for tracker in self.car_trackers:
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

            if have_intersection(tracker[0].current_box, self.left_gate_finish) and tracker[0].direction == "L":
                self.remove_near_car(self.left_gate_finish)
                t = time.time() - tracker[0].init_time
                speed = self.left_len / t * 3600
                print("removed left. speed: " + str(speed) + " (км/год)")
                if speed < 200:
                    self.left_speeds.append(speed)
                    self.last_left_speed = speed

            if have_intersection(tracker[0].current_box, self.right_gate_finish) and tracker[0].direction == "R":
                self.remove_near_car(self.right_gate_finish)
                t = time.time() - tracker[0].init_time
                speed = self.right_len / t * 3600
                print("removed right. speed: " + str(speed) + " (км/год)")
                if speed < 200:
                    self.right_speeds.append(speed)
                    self.last_right_speed = speed
        if(len(self.left_speeds)>0):
            cv2.putText(resized_frame, ("{:10.2f}".format(sum(self.left_speeds)/len(self.left_speeds)) + " (km/h) - avarage"), (self.left_gate_finish[0] - 50, self.left_gate_finish[1]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,255,255),2)
        if(len(self.right_speeds)>0):
            cv2.putText(resized_frame, ("{:10.2f}".format(sum(self.right_speeds)/len(self.right_speeds)) + " (km/h) - avarage"), (self.right_gate_finish[0] - 50, self.right_gate_finish[1]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,255,255),2) 
        if(self.last_left_speed>0):
            cv2.putText(resized_frame, ("{:10.2f}".format(self.last_left_speed) + " (km/h) - last"), (self.left_gate_finish[0] - 50, self.left_gate_finish[1]-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),2)
        if(self.last_right_speed>0):
            cv2.putText(resized_frame, ("{:10.2f}".format(self.last_right_speed) + " (km/h) - last"), (self.right_gate_finish[0] - 50, self.right_gate_finish[1]-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),2)
        cv2.imshow("Title", resized_frame) 

def have_intersection(a,b):
    x = max(a[0], b[0])
    y = max(a[1], b[1])
    w = min(a[0]+a[2], b[0]+b[2]) - x
    h = min(a[1]+a[3], b[1]+b[3]) - y
    if w<0 or h<0: return False 
    return True

def main():
    video_url ='rtsp://Oleksii:eLtGk4Cb@31.42.173.15:8072'
    #video_url = 'D:\129.webm'
    tracker = cars_tracker(video_url)
    i = 0    
    while tracker.video.isOpened():
        if i < 3:
            tracker.update()
            i += 1
        else: i = 0
        input_key = cv2.waitKey(1)
        if input_key == 27: 
            break # Exit if ESC pressed        
        if input_key & 0xFF == ord('a'): # a - add new box
            try:
                rand_x = randint(50, tracker.frame_weight - 50)
                rand_y = randint(50, tracker.frame_height - 50)
                box = (rand_x, rand_y, 40, 40)
                tracker.add_car(box, "L")
            except: pass
        if input_key & 0xFF == ord('d'): # a - add new box
            try:
                tracker.remove_car()
            except: pass
    cv2.destroyAllWindows()



if __name__ == '__main__':
    main()