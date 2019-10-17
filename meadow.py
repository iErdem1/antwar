from random import randint
from anthills import *
from cell import Cell
from uuid import uuid4
from itertools import *
from pprint import pprint


class Meadow:
    def __init__(self, size):
        self.size = size
        self.grid = [[Cell() for i in range(self.size)] for i in range(self.size)]
        self.corner_flag(self.grid)
        self.side_flag(self.grid)

        self.queen1 = Queen("Adele")
        self.queen2 = Queen("Elizabeth")
        self.queen3 = Queen("Sik")

        self.hill_number = 3

        self.choose_cell(self.queen1)
        self.choose_cell(self.queen2)
        self.choose_cell(self.queen3)
        self.info = """
            Welcome to the Anthill Simulation!
            ----------------------------------
            - You virtual grid has been created according to your driver code command!
            - 3 Builder Queen object has released and built their own Anthills with same as
            their names. Those are respectively {q_name1}, {q_name2} and {q_name3}.
            - Ant's unique ID includes their Queen's name plus randomly generated uuid4 part.
            - Each grid element includes Cell object to manage created virtual meadow.
            - Basically simulation continues until one Anthill remains.
            - Initially, all anthills have some rooms and ants equally to start.
            - You may see Cell objects side and corner flags in the source code. We use these
            flags to keep ants inside the meadow.
            - When 2 ant's road crossed, some possible fight scenerios might be occur:
                 If warrior attacks an forager, they have 50% chance to win equally .
                 If a warrior attacks a hill, has 20% chance to destroy.
        """
        self.cycle(self.grid)

    def choose_cell(self, q_obj):
        tmp_obj = self.grid[q_obj.choose_row][q_obj.choose_col]
        tmp_obj.hill_flag = True
        tmp_obj.anthill_name = q_obj.anthill.anthill_name
        q_obj.anthill.food_number = tmp_obj.food

        for i in range(q_obj.anthill.worker_number):
            self.w_ant = WorkerAnt()
            self.w_ant.base_cell_row = q_obj.choose_row
            self.w_ant.base_cell_col = q_obj.choose_col
            self.gen_ant_id(q_obj.anthill, self.w_ant)
            tmp_obj.ants.append(self.w_ant)
            tmp_obj.worker_ants.append(self.w_ant)
            self.w_ant.hill_id = q_obj.anthill.anthill_name

    def create_room(self, layout, q_obj):
        decision = randint(0, 2)
        self.room = None
        self.index = None
        if decision == 0 and q_obj.anthill.food_number > 0:
            self.room = WorkerRoom()
            print("A WorkerRoom created in Anthill: {}.".format(q_obj.anthill.anthill_name))
            q_obj.anthill.food_number -= 1
            q_obj.anthill.room_number += 1
            q_obj.anthill.worker_number -= 1
            q_obj.anthill.ant_number -= 1
            q_obj.anthill.rooms.append(self.room)
            tmp_obj = layout[q_obj.choose_row][q_obj.choose_col]
            tmp_ant_obj = tmp_obj.worker_ants[len(tmp_obj.worker_ants) - 1]
            tmp_ant_id = tmp_ant_obj.ant_id
            for i in range(len(tmp_obj.ants)):
                if tmp_obj.ants[i].ant_id == tmp_ant_id:
                    self.index = i
                    deleted_ant = tmp_obj.ants.pop(self.index)
                    del deleted_ant
            del tmp_ant_obj

        elif decision == 1 and q_obj.anthill.food_number > 0:
            self.room = ForagerRoom()
            print("A ForagerRoom created in Anthill: {}.".format(q_obj.anthill.anthill_name))
            q_obj.anthill.food_number -= 1
            q_obj.anthill.room_number += 1
            q_obj.anthill.worker_number -= 1
            q_obj.anthill.ant_number -= 1
            q_obj.anthill.rooms.append(self.room)
            tmp_obj = layout[q_obj.choose_row][q_obj.choose_col]
            tmp_ant_obj = tmp_obj.worker_ants[len(tmp_obj.worker_ants) - 1]
            tmp_ant_id = tmp_ant_obj.ant_id
            for i in range(len(tmp_obj.ants)):
                if tmp_obj.ants[i].ant_id == tmp_ant_id:
                    self.index = i
                    deleted_ant = tmp_obj.ants.pop(self.index)
            del deleted_ant
            del tmp_ant_obj

        elif decision == 2 and q_obj.anthill.food_number > 0:
            self.room = WarriorRoom()
            print("A WarriorRoom created in Anthill: {}.".format(q_obj.anthill.anthill_name))
            q_obj.anthill.food_number -= 1
            q_obj.anthill.room_number += 1
            q_obj.anthill.worker_number -= 1
            q_obj.anthill.ant_number -= 1
            q_obj.anthill.rooms.append(self.room)
            tmp_obj = layout[q_obj.choose_row][q_obj.choose_col]
            tmp_ant_obj = tmp_obj.worker_ants[len(tmp_obj.worker_ants) - 1]
            tmp_ant_id = tmp_ant_obj.ant_id
            for i in range(len(tmp_obj.ants)):
                if tmp_obj.ants[i].ant_id == tmp_ant_id:
                    self.index = i
            deleted_ant = tmp_obj.ants.pop(self.index)
            del tmp_ant_obj
            del deleted_ant

    def corner_flag(self, layout):
        for i in range(self.size):
            for j in range(self.size):
                while i < self.size:
                    if i == 0 and j == 0:
                        layout[i][j].up_left_corner_flag = True
                        break
                    elif i == self.size - 1 and j == self.size - 1:
                        layout[i][j].down_right_corner_flag = True
                        break
                    elif i == 0 and j == self.size - 1:
                        layout[i][j].down_left_corner_flag = True
                        break
                    elif i == self.size - 1 and j == 0:
                        layout[i][j].up_right_corner_flag = True
                        break
                    else:
                        break

    def side_flag(self, layout):
        for i in range(self.size):
            for j in range(self.size):
                while i > 0 or i < self.size:
                    if self.size - 1 > i > 0 and j == 0:
                        layout[i][j].left_side_flag = True
                        break
                    elif i == 0 and self.size - 2 >= j > 0:
                        layout[i][j].up_side_flag = True
                        break
                    elif i == self.size - 1 and 0 < j <= self.size - 2:
                        layout[i][j].down_side_flag = True
                        break
                    elif 0 < i <= self.size - 2 and j == self.size - 1:
                        layout[i][j].right_side_flag = True
                        break
                    else:
                        break

    def try_conquer(self, w_ant, hill):
        if hill.anthill_name != w_ant.hill_id:
            chance = randint(0, 4)
            if chance == 0:
                print("Warrior ant {ant_id} from {war_hill} destroyed the {ant_hill}!"
                      .format(ant_id=w_ant.ant_id, war_hill=w_ant.hill_id, ant_hill=hill.anthill_name))
                del hill
                self.hill_number -= 1
            else:
                print("Warrior ant {ant_id} from {war_hill} killed by enemy forces."
                      .format(ant_id=w_ant.ant_id, war_hill=w_ant.hill_id))
                del w_ant

    def fight(self, ant1, ant2):
        if isinstance(ant1, ForagerAnt) and isinstance(ant2, WarriorAnt):
            if ant1.hill_id != ant2.hill_id:
                chance_of_living = randint(0, 1)
                if chance_of_living < 1:
                    del ant1
                else:
                    print("Forager with id {} from {} anthill survived!".format(ant1.ant_id, ant1.hill_id))
        elif isinstance(ant1, WarriorAnt) and isinstance(ant2, ForagerAnt):
            if ant1.hill_id != ant2.hill_id:
                chance_of_living = randint(0, 1)
                if chance_of_living < 1:
                    del ant2
                else:
                    print("Forager with id {} from {} anthill survived!".format(ant2.ant_id, ant2.hill_id))
        elif isinstance(ant1, WarriorAnt) and isinstance(ant2, WarriorAnt):
            if ant1.hill_id != ant2.hill_id:
                print("Warrior{} from anthil: {} and Warrior{} from anthil: {} are fighting".format(ant1.ant_id,
                                                                                                    ant1.hill_id,
                                                                                                    ant2.ant_id,
                                                                                                    ant2.hill_id))
                while ant1.defence > 0 and ant2.defence > 0:
                    ant2.defence -= ant1.hit
                    ant1.defence -= ant2.hit
                    if ant1.defence < 0 and ant2.defence > 0:
                        self.do_attributes(ant2)
                        print("Warrior{} from anthill: {} lost against Warrior{} from anthill: {}".format(ant1.ant_id,
                                                                                                          ant1.hill_id,
                                                                                                          ant2.ant_id,
                                                                                                          ant2.hill_id))
                        print("Warrior{} from anthil: {} is gained 10 extra hit point its new hit point is : {}".format(ant2.ant_id,
                                                                                                                        ant2.hill_id,
                                                                                                                        ant2.hit))
                        print("Warrior{} from anthil: {} is gained 10 extra defence point its new defence is : {}".format(ant2.ant_id,
                                                                                                                          ant2.hill_id,
                                                                                                                          ant2.defence))
                        del ant1
                        break
                    elif ant2.defence < 0 and ant1.defence > 0:
                        self.do_attributes(ant1)
                        print("Warrior{} from anthill: {} lost against Warrior{} from anthill: {}".format(ant2.ant_id,
                                                                                                          ant2.hill_id,
                                                                                                          ant1.ant_id,
                                                                                                          ant1.hill_id))
                        print("Warrior{} from anthil: {} is gained 10 extra hit point its new hit point is : {}".format(ant1.ant_id,
                                                                                                                        ant1.hill_id,
                                                                                                                        ant1.hit))
                        print("Warrior{} from anthil: {} is gained 10 extra defence point its new defence is : {}".format(ant1.ant_id,
                                                                                                                          ant1.hill_id,
                                                                                                                          ant1.defence))

                        del ant2
                        break
                    else:
                        print("Warrior{} and Warrior{} killed each other".format(ant1.ant_id, ant2.ant_id))
                        del ant1
                        del ant2
                        break

    def do_attributes(self, ant_obj):
        ant_obj.gain_attributes()

    def move(self, layout):
        self.choose_side = None
        self.tmp_index = None
        for i in range(self.size):
            for j in range(self.size):
                if len(layout[i][j].ants) > 0:
                    for ant in layout[i][j].ants:
                        if not isinstance(ant, WorkerAnt):
                            if ant in layout[i][j].forager_with_food:
                                break
                            else:
                                if layout[i][j].up_left_corner_flag:
                                    self.choose_side = randint(0, 1)
                                    if self.choose_side == 0:
                                        self.move_right(ant)
                                        ant.directions.append('r')
                                        ant.reverse_dir.insert(0, 'l')
                                        self.tmp_index = layout[i][j].ants.index(ant)
                                        layout[i][j+1].ants.append(layout[i][j].ants.pop(self.tmp_index))
                                    else:
                                        self.move_down(ant)
                                        ant.directions.append('d')
                                        ant.reverse_dir.insert(0, 'u')
                                        self.tmp_index = layout[i][j].ants.index(ant)
                                        layout[i+1][j].ants.append(layout[i][j].ants.pop(self.tmp_index))

                                elif layout[i][j].up_right_corner_flag:
                                    self.choose_side = randint(0, 1)
                                    if self.choose_side == 0:
                                        self.move_left(ant)
                                        ant.directions.append('l')
                                        ant.reverse_dir.insert(0, 'r')
                                        self.tmp_index = layout[i][j].ants.index(ant)
                                        layout[i][j - 1].ants.append(layout[i][j].ants.pop(self.tmp_index))
                                    else:
                                        self.move_down(ant)
                                        self.tmp_index = layout[i][j].ants.index(ant)
                                        ant.directions.append('d')
                                        ant.reverse_dir.insert(0, 'u')
                                        layout[i + 1][j].ants.append(layout[i][j].ants.pop(self.tmp_index))

                                elif layout[i][j].down_left_corner_flag:
                                    self.choose_side = randint(0, 1)
                                    if self.choose_side == 0:
                                        self.move_up(ant)
                                        ant.directions.append('u')
                                        ant.reverse_dir.insert(0, 'd')
                                        self.tmp_index = layout[i][j].ants.index(ant)
                                        layout[i - 1][j].ants.append(layout[i][j].ants.pop(self.tmp_index))
                                    else:
                                        self.move_right(ant)
                                        ant.directions.append('r')
                                        ant.reverse_dir.insert(0, 'l')
                                        self.tmp_index = layout[i][j].ants.index(ant)
                                        layout[i][j + 1].ants.append(layout[i][j].ants.pop(self.tmp_index))

                                elif layout[i][j].down_right_corner_flag:
                                    self.choose_side = randint(0, 1)
                                    if self.choose_side == 0:
                                        self.move_up(ant)
                                        ant.directions.append('u')
                                        ant.reverse_dir.insert(0, 'd')
                                        self.tmp_index = layout[i][j].ants.index(ant)
                                    else:
                                        self.move_left(ant)
                                        ant.directions.append('l')
                                        ant.reverse_dir.insert(0, 'r')
                                        self.tmp_index = layout[i][j].ants.index(ant)
                                        layout[i][j - 1].ants.append(layout[i][j].ants.pop(self.tmp_index))

                                elif layout[i][j].up_side_flag:
                                    self.choose_side = randint(0, 2)
                                    if self.choose_side == 0:
                                        self.move_left(ant)
                                        ant.directions.append('l')
                                        ant.reverse_dir.insert(0, 'r')
                                        self.tmp_index = layout[i][j].ants.index(ant)
                                        layout[i][j - 1].ants.append(layout[i][j].ants.pop(self.tmp_index))
                                    elif self.choose_side == 1:
                                        self.move_right(ant)
                                        ant.directions.append('r')
                                        ant.reverse_dir.insert(0, 'l')
                                        self.tmp_index = layout[i][j].ants.index(ant)
                                        layout[i][j + 1].ants.append(layout[i][j].ants.pop(self.tmp_index))
                                    else:
                                        self.move_down(ant)
                                        ant.directions.append('d')
                                        ant.reverse_dir.insert(0, 'u')
                                        self.tmp_index = layout[i][j].ants.index(ant)
                                        layout[i + 1][j].ants.append(layout[i][j].ants.pop(self.tmp_index))

                                elif layout[i][j].left_side_flag:
                                    self.choose_side = randint(0, 2)
                                    if self.choose_side == 0:
                                        self.move_up(ant)
                                        ant.directions.append('u')
                                        ant.reverse_dir.insert(0, 'd')
                                        self.tmp_index = layout[i][j].ants.index(ant)
                                        layout[i - 1][j].ants.append(layout[i][j].ants.pop(self.tmp_index))
                                    elif self.choose_side == 1:
                                        self.move_right(ant)
                                        ant.directions.append('r')
                                        ant.reverse_dir.insert(0, 'l')
                                        self.tmp_index = layout[i][j].ants.index(ant)
                                        layout[i][j + 1].ants.append(layout[i][j].ants.pop(self.tmp_index))
                                    else:
                                        self.move_down(ant)
                                        ant.directions.append('d')
                                        ant.reverse_dir.insert(0, 'u')
                                        self.tmp_index = layout[i][j].ants.index(ant)
                                        layout[i + 1][j].ants.append(layout[i][j].ants.pop(self.tmp_index))

                                elif layout[i][j].down_side_flag:
                                    self.choose_side = randint(0, 2)
                                    if self.choose_side == 0:
                                        self.move_left(ant)
                                        ant.directions.append('l')
                                        ant.reverse_dir.insert(0, 'r')
                                        self.tmp_index = layout[i][j].ants.index(ant)
                                        layout[i][j - 1].ants.append(layout[i][j].ants.pop(self.tmp_index))
                                    elif self.choose_side == 1:
                                        self.move_right(ant)
                                        ant.directions.append('r')
                                        ant.reverse_dir.insert(0, 'l')
                                        self.tmp_index = layout[i][j].ants.index(ant)
                                        layout[i][j + 1].ants.append(layout[i][j].ants.pop(self.tmp_index))
                                    else:
                                        self.move_up(ant)
                                        ant.directions.append('u')
                                        ant.reverse_dir.insert(0, 'd')
                                        self.tmp_index = layout[i][j].ants.index(ant)
                                        layout[i - 1][j].ants.append(layout[i][j].ants.pop(self.tmp_index))

                                elif layout[i][j].right_side_flag:
                                    self.choose_side = randint(0, 2)
                                    if self.choose_side == 0:
                                        self.move_left(ant)
                                        ant.directions.append('l')
                                        ant.reverse_dir.insert(0, 'r')
                                        self.tmp_index = layout[i][j].ants.index(ant)
                                        layout[i][j - 1].ants.append(layout[i][j].ants.pop(self.tmp_index))
                                    elif self.choose_side == 1:
                                        self.move_up(ant)
                                        ant.directions.append('u')
                                        ant.reverse_dir.insert(0, 'd')
                                        self.tmp_index = layout[i][j].ants.index(ant)
                                        layout[i - 1][j].ants.append(layout[i][j].ants.pop(self.tmp_index))
                                    else:
                                        self.move_down(ant)
                                        ant.directions.append('d')
                                        ant.reverse_dir.insert(0, 'u')
                                        self.tmp_index = layout[i][j].ants.index(ant)
                                        layout[i + 1][j].ants.append(layout[i][j].ants.pop(self.tmp_index))

                                else:
                                    self.choose_side = randint(0, 3)
                                    if self.choose_side == 0:
                                        self.move_right(ant)
                                        ant.directions.append('r')
                                        ant.reverse_dir.insert(0, 'l')
                                        self.tmp_index = layout[i][j].ants.index(ant)
                                        layout[i][j+1].ants.append(layout[i][j].ants.pop(self.tmp_index))

                                    elif self.choose_side == 1:
                                        self.move_left(ant)
                                        ant.directions.append('l')
                                        ant.reverse_dir.insert(0, 'r')
                                        self.tmp_index = layout[i][j].ants.index(ant)
                                        layout[i][j-1].ants.append(layout[i][j].ants.pop(self.tmp_index))

                                    elif self.choose_side == 2:
                                        self.move_up(ant)
                                        ant.directions.append('u')
                                        ant.reverse_dir.insert(0, 'd')
                                        self.tmp_index = layout[i][j].ants.index(ant)
                                        layout[i-1][j].ants.append(layout[i][j].ants.pop(self.tmp_index))

                                    else:
                                        self.move_down(ant)
                                        ant.directions.append('d')
                                        ant.reverse_dir.insert(0, 'u')
                                        self.tmp_index = layout[i][j].ants.index(ant)
                                        layout[i+1][j].ants.append(layout[i][j].ants.pop(self.tmp_index))

    def move_back(self, layout):
        self.tmp_index = None
        for i in range(self.size):
            for j in range(self.size):
                if len(layout[i][j].forager_with_food) <= 0:
                    break
                else:
                    for ant in layout[i][j].forager_with_food:
                        for direct in ant.reverse_dir:
                            if direct == 'r':
                                self.move_right(ant)
                                self.tmp_index = layout[i][j].forager_with_food.index(ant)
                                layout[i][j+1].forager_with_food.append(layout[i][j].forager_with_food.pop(self.tmp_index))
                                if ant.base_cell_row == ant.current_cell_row and ant.base_cell_col == ant.current_cell_col:
                                    layout[ant.base_cell_row][ant.base_cell_col].food += 1
                                    self.tmp = layout[ant.base_cell_row][ant.base_cell_col].forager_with_food.index(ant)
                                    layout[ant.base_cell_row][ant.base_cell_col].ants.append(layout[ant.base_cell_row][ant.base_cell_col].forager_with_food.pop(self.tmp))

                            elif direct == 'l':
                                self.move_left(ant)
                                self.tmp_index = layout[i][j].forager_with_food.index(ant)
                                layout[i][j-1].forager_with_food.append(layout[i][j].forager_with_food.pop(self.tmp_index))
                                if ant.base_cell_row == ant.current_cell_row and ant.base_cell_col == ant.current_cell_col:
                                    layout[ant.base_cell_row][ant.base_cell_col].food += 1
                                    self.tmp = layout[ant.base_cell_row][ant.base_cell_col].forager_with_food.index(ant)
                                    layout[ant.base_cell_row][ant.base_cell_col].ants.append(layout[ant.base_cell_row][ant.base_cell_col].forager_with_food.pop(self.tmp))

                            elif direct == 'u':
                                self.move_up(ant)
                                self.tmp_index = layout[i][j].forager_with_food.index(ant)
                                layout[i-1][j].forager_with_food.append(layout[i][j].forager_with_food.pop(self.tmp_index))
                                if ant.base_cell_row == ant.current_cell_row and ant.base_cell_col == ant.current_cell_col:
                                    layout[ant.base_cell_row][ant.base_cell_col].food += 1
                                    self.tmp = layout[ant.base_cell_row][ant.base_cell_col].forager_with_food.index(ant)
                                    layout[ant.base_cell_row][ant.base_cell_col].ants.append(layout[ant.base_cell_row][ant.base_cell_col].forager_with_food.pop(self.tmp))

                            else:
                                self.move_down(ant)
                                self.tmp_index = layout[i][j].forager_with_food.index(ant)
                                layout[i+1][j].forager_with_food.append(layout[i][j].forager_with_food.pop(self.tmp_index))
                                if ant.base_cell_row == ant.current_cell_row and ant.base_cell_col == ant.current_cell_col:
                                    layout[ant.base_cell_row][ant.base_cell_col].food += 1
                                    self.tmp = layout[ant.base_cell_row][ant.base_cell_col].forager_with_food.index(ant)
                                    layout[ant.base_cell_row][ant.base_cell_col].ants.append(layout[ant.base_cell_row][ant.base_cell_col].forager_with_food.pop(self.tmp))
                                
    def gen_ant_id(self, hill, ant):
        hill_part = hill.anthill_name
        rand_part = str(uuid4())
        rand_part = rand_part[0:12]
        unique = hill_part + rand_part
        ant.ant_id = unique

    def move_up(self, ant_obj):
        ant_obj.current_cell_row -= 1

    def move_down(self, ant_obj):
        ant_obj.current_cell_row += 1

    def move_left(self, ant_obj):
        ant_obj.current_cell_col -= 1

    def move_right(self, ant_obj):
        ant_obj.current_cell_col += 1

    def collect_food(self, ant):
        ant.collected_food += 1

    def cycle(self, layout):
        print(self.info)
        self.produced_ant = None

        user_input = input("Options: 1) See result of the simulation."
                           "         2) Enter a cycle number to simulate.")

        if user_input == "1":
            while self.hill_number >= 1:
                for i in range(self.size):
                    for j in range(self.size):
                        if layout[i][j].hill_flag:
                            if layout[i][j].food > 0 and len(layout[i][j].worker_ants) > 0:
                                if layout[i][j].anthill_name == "Adele":
                                    self.create_room(layout, self.queen1)
                                elif layout[i][j].anthill_name == "Elizabeth":
                                    self.create_room(layout, self.queen2)
                                else:
                                    self.create_room(layout, self.queen3)
                            if len(layout[i][j].ants) <= self.size:
                                if layout[i][j].anthill_name == "Adele":
                                    if len(layout[i][j].worker_ants) > len(self.queen1.anthill.rooms):
                                        for k in range(len(self.queen1.anthill.rooms)):
                                            tmp_room = self.queen1.anthill.rooms[k]
                                            self.produced_ant = tmp_room.produce_ant()
                                            self.produced_ant.hill_id = self.queen1.queen_name
                                            self.produced_ant.base_cell_row = self.queen1.choose_row
                                            self.produced_ant.base_cell_col = self.queen1.choose_col
                                            self.produced_ant.current_cell_row = self.queen1.choose_row
                                            self.produced_ant.current_cell_col = self.queen1.choose_col
                                            self.gen_ant_id(self.queen1.anthill, self.produced_ant)
                                            layout[i][j].ants.append(self.produced_ant)
                                            if self.produced_ant.ant_type == "worker":
                                                layout[i][j].worker_ants.append(self.produced_ant)
                                    elif len(layout[i][j].worker_ants) < len(self.queen1.anthill.rooms):
                                        for k in range(len(layout.worker_ants)):
                                            tmp_room = self.queen1.anthill.rooms[k]
                                            self.produced_ant = tmp_room.produce_ant()
                                            self.produced_ant.hill_id = self.queen1.queen_name
                                            self.produced_ant.base_cell_row = self.queen1.choose_row
                                            self.produced_ant.base_cell_col = self.queen1.choose_col
                                            self.produced_ant.current_cell_row = self.queen1.choose_row
                                            self.produced_ant.current_cell_col = self.queen1.choose_col
                                            self.gen_ant_id(self.queen1.anthill, self.produced_ant)
                                            layout[i][j].ants.append(self.produced_ant)
                                            if self.produced_ant.ant_type == "worker":
                                                layout[i][j].worker_ants.append(self.produced_ant)
                                    else:
                                        for k in range(len(layout.worker_ants)):
                                            tmp_room = self.queen1.anthill.rooms[k]
                                            self.produced_ant = tmp_room.produce_ant()
                                            self.produced_ant.hill_id = self.queen1.queen_name
                                            self.produced_ant.base_cell_row = self.queen1.choose_row
                                            self.produced_ant.base_cell_col = self.queen1.choose_col
                                            self.produced_ant.current_cell_row = self.queen1.choose_row
                                            self.produced_ant.current_cell_col = self.queen1.choose_col
                                            self.gen_ant_id(self.queen1.anthill, self.produced_ant)
                                            layout[i][j].ants.append(self.produced_ant)
                                            if self.produced_ant.ant_type == "worker":
                                                layout[i][j].worker_ants.append(self.produced_ant)
                                elif layout[i][j].anthill_name == "Elizabeth":
                                    if len(layout[i][j].worker_ants) > len(self.queen2.anthill.rooms):
                                        for k in range(len(self.queen2.anthill.rooms)):
                                            tmp_room = self.queen2.anthill.rooms[k]
                                            self.produced_ant = tmp_room.produce_ant()
                                            self.produced_ant.hill_id = self.queen2.queen_name
                                            self.produced_ant.base_cell_row = self.queen2.choose_row
                                            self.produced_ant.base_cell_col = self.queen2.choose_col
                                            self.produced_ant.current_cell_row = self.queen2.choose_row
                                            self.produced_ant.current_cell_col = self.queen2.choose_col
                                            self.gen_ant_id(self.queen2.anthill, self.produced_ant)
                                            layout[i][j].ants.append(self.produced_ant)
                                            if self.produced_ant.ant_type == "worker":
                                                layout[i][j].worker_ants.append(self.produced_ant)
                                    elif len(layout[i][j].worker_ants) < len(self.queen1.anthill.rooms):
                                        for k in range(len(layout.worker_ants)):
                                            tmp_room = self.queen2.anthill.rooms[k]
                                            self.produced_ant = tmp_room.produce_ant()
                                            self.produced_ant.hill_id = self.queen2.queen_name
                                            self.produced_ant.base_cell_row = self.queen2.choose_row
                                            self.produced_ant.base_cell_col = self.queen2.choose_col
                                            self.produced_ant.current_cell_row = self.queen2.choose_row
                                            self.produced_ant.current_cell_col = self.queen2.choose_col
                                            self.gen_ant_id(self.queen2.anthill, self.produced_ant)
                                            layout[i][j].ants.append(self.produced_ant)
                                            if self.produced_ant.ant_type == "worker":
                                                layout[i][j].worker_ants.append(self.produced_ant)
                                    else:
                                        for k in range(len(layout.worker_ants)):
                                            tmp_room = self.queen2.anthill.rooms[k]
                                            self.produced_ant = tmp_room.produce_ant()
                                            self.produced_ant.hill_id = self.queen2.queen_name
                                            self.produced_ant.base_cell_row = self.queen2.choose_row
                                            self.produced_ant.base_cell_col = self.queen2.choose_col
                                            self.produced_ant.current_cell_row = self.queen2.choose_row
                                            self.produced_ant.current_cell_col = self.queen2.choose_col
                                            self.gen_ant_id(self.queen2.anthill, self.produced_ant)
                                            layout[i][j].ants.append(self.produced_ant)
                                            if self.produced_ant.ant_type == "worker":
                                                layout[i][j].worker_ants.append(self.produced_ant)
                                else:
                                    if len(layout[i][j].worker_ants) > len(self.queen3.anthill.rooms):
                                        for k in range(len(self.queen3.anthill.rooms)):
                                            tmp_room = self.queen3.anthill.rooms[k]
                                            self.produced_ant = tmp_room.produce_ant()
                                            self.produced_ant.hill_id = self.queen3.queen_name
                                            self.produced_ant.base_cell_row = self.queen3.choose_row
                                            self.produced_ant.base_cell_col = self.queen3.choose_col
                                            self.produced_ant.current_cell_row = self.queen3.choose_row
                                            self.produced_ant.current_cell_col = self.queen3.choose_col
                                            self.gen_ant_id(self.queen3.anthill, self.produced_ant)
                                            layout[i][j].ants.append(self.produced_ant)
                                            if self.produced_ant.ant_type == "worker":
                                                layout[i][j].worker_ants.append(self.produced_ant)
                                    elif len(layout[i][j].worker_ants) < len(self.queen1.anthill.rooms):
                                        for k in range(len(layout.worker_ants)):
                                            tmp_room = self.queen3.anthill.rooms[k]
                                            self.produced_ant = tmp_room.produce_ant()
                                            self.produced_ant.hill_id = self.queen3.queen_name
                                            self.produced_ant.base_cell_row = self.queen3.choose_row
                                            self.produced_ant.base_cell_col = self.queen3.choose_col
                                            self.produced_ant.current_cell_row = self.queen3.choose_row
                                            self.produced_ant.current_cell_col = self.queen3.choose_col
                                            self.gen_ant_id(self.queen3.anthill, self.produced_ant)
                                            layout[i][j].ants.append(self.produced_ant)
                                            if self.produced_ant.ant_type == "worker":
                                                layout[i][j].worker_ants.append(self.produced_ant)
                                    else:
                                        for k in range(len(layout.worker_ants)):
                                            tmp_room = self.queen3.anthill.rooms[k]
                                            self.produced_ant = tmp_room.produce_ant()
                                            self.produced_ant.hill_id = self.queen3.queen_name
                                            self.produced_ant.base_cell_row = self.queen3.choose_row
                                            self.produced_ant.base_cell_col = self.queen3.choose_col
                                            self.produced_ant.current_cell_row = self.queen3.choose_row
                                            self.produced_ant.current_cell_col = self.queen3.choose_col
                                            self.gen_ant_id(self.queen3.anthill, self.produced_ant)
                                            layout[i][j].ants.append(self.produced_ant)
                                            if self.produced_ant.ant_type == "worker":
                                                layout[i][j].worker_ants.append(self.produced_ant)
                self.move(layout)

                for i in range(self.size):
                    for j in range(self.size):
                        for ant in layout[i][j].ants:
                            tmp_index = layout[i][j].ants.index(ant)
                            if isinstance(ant, ForagerAnt):
                                if layout[i][j].food > 0:
                                    self.collect_food(ant)
                                    layout[i][j].food -= 1
                                    layout[i][j].forager_with_food.append(ant)
                                    self.move_back(layout)
                        comb = list(combinations(layout[i][j].ants, 2))

                        for k in range(len(comb)):
                            self.fight(comb[k][0], comb[k][1])

                        if layout[i][j].hill_flag:
                            if layout[i][j].anthill_name == "Adele":
                                for ant in layout[i][j].ants:
                                    if isinstance(ant, WarriorAnt):
                                        self.try_conquer(ant, self.queen1.anthill)
                            elif layout[i][j].anthill_name == "Elizabeth":
                                for ant in layout[i][j].ants:
                                    if isinstance(ant, WarriorAnt):
                                        self.try_conquer(ant, self.queen2.anthill)
                            elif layout[i][j].anthill_name == "Sik":
                                for ant in layout[i][j].ants:
                                    if isinstance(ant, WarriorAnt):
                                        self.try_conquer(ant, self.queen3.anthill)



        if user_input == '2':
            self.cycle_input = int(input("Cycle number:"))
            self.c_counter = 1
            while self.cycle_input > 0:
                print("{}. cycle".format(self.c_counter))
                for i in range(self.size):
                    for j in range(self.size):
                        if layout[i][j].hill_flag:
                            if layout[i][j].food > 0 and len(layout[i][j].worker_ants) > 0:
                                if layout[i][j].anthill_name == "Adele":
                                    self.create_room(layout, self.queen1)
                                elif layout[i][j].anthill_name == "Elizabeth":
                                    self.create_room(layout, self.queen2)
                                else:
                                    self.create_room(layout, self.queen3)
                            if len(layout[i][j].ants) <= self.size:
                                if layout[i][j].anthill_name == "Adele":
                                    if len(layout[i][j].worker_ants) > len(self.queen1.anthill.rooms):
                                        for k in range(len(self.queen1.anthill.rooms)):
                                            tmp_room = self.queen1.anthill.rooms[k]
                                            self.produced_ant = tmp_room.produce_ant()
                                            self.produced_ant.hill_id = self.queen1.queen_name
                                            self.produced_ant.base_cell_row = self.queen1.choose_row
                                            self.produced_ant.base_cell_col = self.queen1.choose_col
                                            self.produced_ant.current_cell_row = self.queen1.choose_row
                                            self.produced_ant.current_cell_col = self.queen1.choose_col
                                            self.gen_ant_id(self.queen1.anthill, self.produced_ant)
                                            layout[i][j].ants.append(self.produced_ant)
                                            if self.produced_ant.ant_type == "worker":
                                                layout[i][j].worker_ants.append(self.produced_ant)
                                    elif len(layout[i][j].worker_ants) < len(self.queen1.anthill.rooms):
                                        for k in range(len(layout.worker_ants)):
                                            tmp_room = self.queen1.anthill.rooms[k]
                                            self.produced_ant = tmp_room.produce_ant()
                                            self.produced_ant.hill_id = self.queen1.queen_name
                                            self.produced_ant.base_cell_row = self.queen1.choose_row
                                            self.produced_ant.base_cell_col = self.queen1.choose_col
                                            self.produced_ant.current_cell_row = self.queen1.choose_row
                                            self.produced_ant.current_cell_col = self.queen1.choose_col
                                            self.gen_ant_id(self.queen1.anthill, self.produced_ant)
                                            layout[i][j].ants.append(self.produced_ant)
                                            if self.produced_ant.ant_type == "worker":
                                                layout[i][j].worker_ants.append(self.produced_ant)
                                    else:
                                        for k in range(len(layout.worker_ants)):
                                            tmp_room = self.queen1.anthill.rooms[k]
                                            self.produced_ant = tmp_room.produce_ant()
                                            self.produced_ant.hill_id = self.queen1.queen_name
                                            self.produced_ant.base_cell_row = self.queen1.choose_row
                                            self.produced_ant.base_cell_col = self.queen1.choose_col
                                            self.produced_ant.current_cell_row = self.queen1.choose_row
                                            self.produced_ant.current_cell_col = self.queen1.choose_col
                                            self.gen_ant_id(self.queen1.anthill, self.produced_ant)
                                            layout[i][j].ants.append(self.produced_ant)
                                            if self.produced_ant.ant_type == "worker":
                                                layout[i][j].worker_ants.append(self.produced_ant)
                                elif layout[i][j].anthill_name == "Elizabeth":
                                    if len(layout[i][j].worker_ants) > len(self.queen2.anthill.rooms):
                                        for k in range(len(self.queen2.anthill.rooms)):
                                            tmp_room = self.queen2.anthill.rooms[k]
                                            self.produced_ant = tmp_room.produce_ant()
                                            self.produced_ant.hill_id = self.queen2.queen_name
                                            self.produced_ant.base_cell_row = self.queen2.choose_row
                                            self.produced_ant.base_cell_col = self.queen2.choose_col
                                            self.produced_ant.current_cell_row = self.queen2.choose_row
                                            self.produced_ant.current_cell_col = self.queen2.choose_col
                                            self.gen_ant_id(self.queen2.anthill, self.produced_ant)
                                            layout[i][j].ants.append(self.produced_ant)
                                            if self.produced_ant.ant_type == "worker":
                                                layout[i][j].worker_ants.append(self.produced_ant)
                                    elif len(layout[i][j].worker_ants) < len(self.queen1.anthill.rooms):
                                        for k in range(len(layout.worker_ants)):
                                            tmp_room = self.queen2.anthill.rooms[k]
                                            self.produced_ant = tmp_room.produce_ant()
                                            self.produced_ant.hill_id = self.queen2.queen_name
                                            self.produced_ant.base_cell_row = self.queen2.choose_row
                                            self.produced_ant.base_cell_col = self.queen2.choose_col
                                            self.produced_ant.current_cell_row = self.queen2.choose_row
                                            self.produced_ant.current_cell_col = self.queen2.choose_col
                                            self.gen_ant_id(self.queen2.anthill, self.produced_ant)
                                            layout[i][j].ants.append(self.produced_ant)
                                            if self.produced_ant.ant_type == "worker":
                                                layout[i][j].worker_ants.append(self.produced_ant)
                                    else:
                                        for k in range(len(layout.worker_ants)):
                                            tmp_room = self.queen2.anthill.rooms[k]
                                            self.produced_ant = tmp_room.produce_ant()
                                            self.produced_ant.hill_id = self.queen2.queen_name
                                            self.produced_ant.base_cell_row = self.queen2.choose_row
                                            self.produced_ant.base_cell_col = self.queen2.choose_col
                                            self.produced_ant.current_cell_row = self.queen2.choose_row
                                            self.produced_ant.current_cell_col = self.queen2.choose_col
                                            self.gen_ant_id(self.queen2.anthill, self.produced_ant)
                                            layout[i][j].ants.append(self.produced_ant)
                                            if self.produced_ant.ant_type == "worker":
                                                layout[i][j].worker_ants.append(self.produced_ant)
                                else:
                                    if len(layout[i][j].worker_ants) > len(self.queen3.anthill.rooms):
                                        for k in range(len(self.queen3.anthill.rooms)):
                                            tmp_room = self.queen3.anthill.rooms[k]
                                            self.produced_ant = tmp_room.produce_ant()
                                            self.produced_ant.hill_id = self.queen3.queen_name
                                            self.produced_ant.base_cell_row = self.queen3.choose_row
                                            self.produced_ant.base_cell_col = self.queen3.choose_col
                                            self.produced_ant.current_cell_row = self.queen3.choose_row
                                            self.produced_ant.current_cell_col = self.queen3.choose_col
                                            self.gen_ant_id(self.queen3.anthill, self.produced_ant)
                                            layout[i][j].ants.append(self.produced_ant)
                                            if self.produced_ant.ant_type == "worker":
                                                layout[i][j].worker_ants.append(self.produced_ant)
                                    elif len(layout[i][j].worker_ants) < len(self.queen1.anthill.rooms):
                                        for k in range(len(layout.worker_ants)):
                                            tmp_room = self.queen3.anthill.rooms[k]
                                            self.produced_ant = tmp_room.produce_ant()
                                            self.produced_ant.hill_id = self.queen3.queen_name
                                            self.produced_ant.base_cell_row = self.queen3.choose_row
                                            self.produced_ant.base_cell_col = self.queen3.choose_col
                                            self.produced_ant.current_cell_row = self.queen3.choose_row
                                            self.produced_ant.current_cell_col = self.queen3.choose_col
                                            self.gen_ant_id(self.queen3.anthill, self.produced_ant)
                                            layout[i][j].ants.append(self.produced_ant)
                                            if self.produced_ant.ant_type == "worker":
                                                layout[i][j].worker_ants.append(self.produced_ant)
                                    else:
                                        for k in range(len(layout.worker_ants)):
                                            tmp_room = self.queen3.anthill.rooms[k]
                                            self.produced_ant = tmp_room.produce_ant()
                                            self.produced_ant.hill_id = self.queen3.queen_name
                                            self.produced_ant.base_cell_row = self.queen3.choose_row
                                            self.produced_ant.base_cell_col = self.queen3.choose_col
                                            self.produced_ant.current_cell_row = self.queen3.choose_row
                                            self.produced_ant.current_cell_col = self.queen3.choose_col
                                            self.gen_ant_id(self.queen3.anthill, self.produced_ant)
                                            layout[i][j].ants.append(self.produced_ant)
                                            if self.produced_ant.ant_type == "worker":
                                                layout[i][j].worker_ants.append(self.produced_ant)
                self.move(layout)
                for i in range(self.size):
                    for j in range(self.size):
                        for ant in layout[i][j].ants:
                            tmp_index = layout[i][j].ants.index(ant)
                            if isinstance(ant, ForagerAnt):
                                if layout[i][j].food > 0:
                                    self.collect_food(ant)
                                    layout[i][j].food -= 1
                                    layout[i][j].forager_with_food.append(layout[i][j].ants.pop(tmp_index))
                                    self.move_back(layout)
                        comb = list(combinations(layout[i][j].ants, 2))

                        for k in range(len(comb)):
                            self.fight(comb[k][0], comb[k][1])

                        if layout[i][j].hill_flag:
                            if layout[i][j].anthill_name == "Adele":
                                for ant in layout[i][j].ants:
                                    if isinstance(ant, WarriorAnt):
                                        self.try_conquer(ant, self.queen1.anthill)
                            elif layout[i][j].anthill_name == "Elizabeth":
                                for ant in layout[i][j].ants:
                                    if isinstance(ant, WarriorAnt):
                                        self.try_conquer(ant, self.queen2.anthill)
                            elif layout[i][j].anthill_name == "Sik":
                                for ant in layout[i][j].ants:
                                    if isinstance(ant, WarriorAnt):
                                        self.try_conquer(ant, self.queen3.anthill)

                self.cycle_input -= 1
                self.c_counter += 1


class Queen:
    def __init__(self, queen_name=None):
        self.queen_name = queen_name
        self.anthill = Anthill(self.queen_name)
        self.choose_col = randint(0, 4)
        self.choose_row = randint(0, 4)
