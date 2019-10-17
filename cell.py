from random import randint


class Cell:
    def __init__(self):
        self.hill_flag = None
        self.anthill_name = None

        self.up_left_corner_flag = False
        self.down_left_corner_flag = False
        self.up_right_corner_flag = False
        self.down_right_corner_flag = False

        self.up_side_flag = False
        self.down_side_flag = False
        self.left_side_flag = False
        self.right_side_flag = False

        self.food = randint(0, 5)
        self.ants = []
        self.worker_ants = []

        self.forager_with_food = []