from random import randint
import time
class car_model:

    def __init__(self, box, direction):
        self.init_box = box
        self.init_time = time.time()
        self.current_box = box
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.box_history = []
        self.direction = direction

    def update_box(self, box):
        self.current_box = box
        if(len(self.box_history) > 100):
            del self.box_history[0]
        self.box_history.append(box)