import pygame
import json
from battle import Battle

class Game:
    def __init__(self):
        # Pygame Settings
        pygame.init()
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        pygame.display.set_caption('RogueLite')
        self.running = True
        self.clock = pygame.time.Clock()
        self.FPS = 30

        # Load characters data from json
        with open("data/characters.json", "r") as f:
            self.characters_data = json.load(f)


        # Team arguments requires the character's name OR id as in the json file - ex. "Ancient Priestess" or 4
        # Both teams need a list as argument, except for a boss. ["Ancient Priestess"] pour un seul non-boss
        self.battle = Battle(self, ["Vasti", "Dryad","Ireza"], 3)

        # Keys variables
        self.escapeKeyDown = False

    def start(self):
        pass


    def loop(self):
        # TO DO :
        # "State Machine" : menu, combat, etc
        while self.running:
            self.eventHandler()
            self.battle.update()
            self.draw()
            self.clock.tick(self.FPS)

    # Draws everything on screen
    def draw(self):
        self.screen.fill('Black')
        self.battle.draw()
        pygame.display.flip()

    # Handles key inputs
    def eventHandler(self):

        for event in pygame.event.get():
            # Exit game
            if event.type == pygame.QUIT:
                self.running = False
            # Get keystrokes
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_SPACE:
                    self.INPUT_Space()
                if event.key == pygame.K_RIGHT:
                    self.INPUT_Right()
            if event.type == pygame.KEYUP:
                keys = pygame.key.get_pressed()

    def INPUT_Space(self):
        # Damages character pointed by the arrow
        self.battle.damageCharacter(self.battle.getTargetedCharacter(),10)
        #self.battle.damageTeam(self.battle.enemyTeam, 60)

    def INPUT_Right(self):
        self.battle.pointer_arrow.advanceToNextPos()