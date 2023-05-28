import pygame
from typing import List, Tuple
from characters import Positions, positions_list
from settings import *

class BattlePointerArrow():
    def __init__(self, pos: List):
        self.img_unscaled = pygame.image.load("images/ui/arrow_blue.png").convert_alpha()
        self.img = pygame.transform.scale(self.img_unscaled, (36,44))
        self.pos_list = pos
        self.current_pos_index = 0
        self.offset = (142, -53)

    def setPos(self, pos: Tuple[int]):
        if pos not in self.pos_list:
            raise ValueError(f'Given position {pos} is not included in the predefined positions list : {self.pos_list}')
        else:
            # Finds index of corresponding position in the list
            for i, value in enumerate(self.pos_list):
                if pos == value:
                    self.current_pos_index = i
        self.checkIfOnBossPos()

    def getPosIndex(self):
        return self.current_pos_index

    def getPosWithOffset(self):
        if self.current_pos_index >= len(self.pos_list):
            self.current_pos_index = 0
            self.offset = (142, -53)
        # Adds together the values of the pos tuple and the offset tuple into another tuple before returning it
        res = tuple(map(lambda i, j: i + j, self.pos_list[self.current_pos_index], self.offset))
        return res


    def advanceToNextPos(self):
        self.current_pos_index += 1
        if self.current_pos_index >= len(self.pos_list):
            self.current_pos_index = 0
        self.checkIfOnBossPos()

    def getImg(self):
        return self.img

    # Modifies offset values if the cursor is pointing the boss (to compensate for bigger sprite)
    def checkIfOnBossPos(self):
        if self.pos_list[self.current_pos_index] == positions_list[Positions.ENEMY_BOSS.value]:
            self.offset = (265, -53)
        else: self.offset = (142, -53)
