from random import randint
class car_model:

    def __init__(self, box):
        self.init_box = box
        self.current_box = box
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.box_history = []

    def update_box(self, box):
        self.current_box = box
        if(len(self.box_history) > 100):
            del self.box_history[0]
        self.box_history.append(box)