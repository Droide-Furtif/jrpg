import pygame
from typing import Tuple, List
from characters import *
from ui import BattlePointerArrow
from settings import *

class Battle:
    def __init__(self, game, allies: List, enemies: List):
        # Loads useful game vars
        self.GAME = game
        self.char_data = self.GAME.characters_data

        # Loads combat images
        self.background_image = pygame.image.load("images/backgrounds/BG_cavelake.png")
        self.background_image = pygame.transform.scale(self.background_image, SCREEN_SIZE)

        # Creates team lists
        self.battlers_list, self.allyTeam, self.enemyTeam = [], [], []
        # Add Characters instances to lists using json data
        self.generateTeams(allies, enemies)

        # Creates pointer arrow ui
        self.pointer_arrow = BattlePointerArrow(Character.updated_positions_list)


    def draw(self):
        # Draw background
        self.GAME.screen.blit(self.background_image, (0, 0))
        # Draw char sprite and health bar below
        for c in self.allyTeam:
            self.GAME.screen.blit(c.getSprite(), (c.getPos()))
            self.GAME.screen.blit(c.getHpBarSurface(), ((c.getPos()[0] -c.getOffset(), c.getPos()[1] + c.img.get_height()+12)))
            if self.GAME.debug_mode:
                rect = pygame.Rect(c.getPos()[0], c.getPos()[1], c.getSprite().get_width(), c.getSprite().get_height())
                pygame.draw.rect(self.GAME.screen, 'red', rect, 5)
        for c in self.enemyTeam:
            self.GAME.screen.blit(c.getSprite(), (c.getPos()))
            self.GAME.screen.blit(c.getHpBarSurface(), ((c.getPos()[0] -c.getOffset(), c.getPos()[1] + c.img.get_height()+12)))
            if self.GAME.debug_mode:
                rect = pygame.Rect(c.getPos()[0], c.getPos()[1], c.getSprite().get_width(), c.getSprite().get_height())
                pygame.draw.rect(self.GAME.screen, 'red', rect, 5)

        # Draws pointer arrow
        self.GAME.screen.blit(self.pointer_arrow.getImg(), self.pointer_arrow.getPosWithOffset())

    # Generates teams lists from arguments and using Game's characters data
    def generateTeams(self, allies, enemies):
        for name in allies:
            char = None
            # Loops over every character data from json until finding one with matching name(str) or id(int)
            for c in self.char_data:
                if name == c["name"] or name == c["id"]:
                    char = Character(c["filename"], True)
            self.allyTeam.append(char)

        # Enemy is a boss if argument isn't a list
        if isinstance(enemies, str) or isinstance(enemies, int):
            for c in self.char_data:
                if enemies == c["name"] or enemies == c["id"]:
                    char = Character(c["filename"], False, True)
            self.enemyTeam.append(char)
        else:
            for name in enemies:
                char = None
                for c in self.char_data:
                    if name == c["name"] or name == c["id"]:
                        char = Character(c["filename"], False)
                self.enemyTeam.append(char)

        self.battlers_list = self.allyTeam + self.enemyTeam

    def damageCharacter(self, char, dmg: int):
        char.takeDamage(dmg)
        if not char.isDead():
            return
        self.battlers_list.remove(char)
        if char.ally == True:
            self.allyTeam.remove(char)
        if char.ally == False:
            self.enemyTeam.remove(char)


    def damageTeam(self, team, dmg: int):
        for c in team:
            self.damageCharacter(c, dmg)


    def update(self):
        pass

    def getTargetedCharacter(self):
        return self.battlers_list[self.pointer_arrow.getPosIndex()]