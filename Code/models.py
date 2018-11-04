from random import randint
class car_model:
    box = ()

    def __init__(self, box):
        self.box = box
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.box_history = []

    def update_box(self, box):
        if(len(self.box_history) > 50):
            del self.box_history[0]
        self.box_history.append(box)