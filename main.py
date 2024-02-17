import pygame
import sys
from utility import load_image
from entities import Enemy, Tower, Bullet, WaveSystem, Map
from menu import *
import time
import random
from pygame.constants import *

# INITIALISATION

pygame.init() # INITIALIZE
pygame.mixer.init() # INITIALIZE

WIDTH = 1000
HEIGHT = 600    
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT)) # sets the screen dimensions to a predetermined WIDTH and HEIGHT var
pygame.display.set_caption("NEA Tower Defence Game") # sets the caption for the game screen

# MUSIC 

# mp3_path = 'Audio\HUMBLE.MP3'

# pygame.init()
# pygame.mixer.init()
# pygame.mixer.music.load(mp3_path)
# pygame.mixer.music.play()

# WAVE INIT

START_WAVE = (USEREVENT + 1)
SPAWN_TOWER_ONE = (USEREVENT + 2)
SPAWN_TOWER_TWO = (USEREVENT + 3)
SPAWN_TOWER_THREE = (USEREVENT + 4)
SPAWN_TOWER_FOUR = (USEREVENT + 5)
SPAWN_ENEMY = (USEREVENT + 6)
END_WAVE = (USEREVENT + 7)

TOWER_ONE_IMAGES = [load_image("characterAttackFrame1.png"), load_image("characterAttackFrame2.png"), load_image("characterAttackFrame3.png"), load_image("characterAttackFrame4.png")]
TOWER_TWO_IMAGES = [load_image("character2AttackFrame1.png"), load_image("character2AttackFrame2.png"), load_image("character2AttackFrame3.png"), load_image("character2AttackFrame4.png")]
TOWER_THREE_IMAGES = [load_image("character3AttackFrame1.png"), load_image("character3AttackFrame2.png"), load_image("character3AttackFrame3.png"), load_image("character3AttackFrame4.png")]
TOWER_FOUR_IMAGES = [load_image("character4AttackFrame1.png"), load_image("character4AttackFrame2.png"), load_image("character4AttackFrame3.png"), load_image("character4AttackFrame4.png")]

ENEMY_ONE_IMAGES = [pygame.transform.flip(load_image("hyenaWalkFrame1.png"), True, False), pygame.transform.flip(load_image("hyenaWalkFrame2.png"), True, False), pygame.transform.flip(load_image("hyenaWalkFrame3.png"), True, False), pygame.transform.flip(load_image("hyenaWalkFrame4.png"), True, False), pygame.transform.flip(load_image("hyenaWalkFrame5.png"), True, False), pygame.transform.flip(load_image("hyenaWalkFrame6.png"), True, False)]
ENEMY_TWO_IMAGES = [load_image("octoWalkFrame1.png"), load_image("octoWalkFrame2.png"), load_image("octoWalkFrame3.png"), load_image("octoWalkFrame4.png"), load_image("octoWalkFrame5.png"), load_image("octoWalkFrame6.png")]

TOWER_ONE = Tower(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], TOWER_ONE_IMAGES, [load_image("fireballFrame1.png"), load_image("fireballFrame2.png"), load_image("fireballFrame3.png"), load_image("fireballFrame4.png")], cost=30, shoot_cooldown=50, dmgOvertime=0, bulletDmg=10, range=600)
TOWER_TWO = Tower(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], TOWER_TWO_IMAGES, [load_image("starFrame1.png"), load_image("starFrame2.png"), load_image("starFrame3.png"), load_image("starFrame4.png")], cost=75, shoot_cooldown=40, dmgOvertime=0, bulletDmg=25)
TOWER_THREE = Tower(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], TOWER_THREE_IMAGES, [load_image("discFrame1.png"), load_image("discFrame2.png"), load_image("discFrame3.png"), load_image("discFrame4.png")], cost=100, shoot_cooldown=10, dmgOvertime=0, bulletDmg=10)
TOWER_FOUR = Tower(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], TOWER_FOUR_IMAGES, [load_image("diamondFrame1.png"), load_image("diamondFrame2.png"), load_image("diamondFrame3.png"), load_image("diamondFrame4.png")], cost=150, shoot_cooldown=10, dmgOvertime=0, bulletDmg=20)

ENEMY_ONE = Enemy(0, 0, random.randint(10, 50), random.randint(10, 17) / 10, ENEMY_ONE_IMAGES, 1)
ENEMY_TWO = Enemy(0, 0, random.randint(100, 150), random.randint(3, 7) / 10, ENEMY_TWO_IMAGES, 4)

# Map Details
DESERT_BACKGROUND = pygame.transform.scale(load_image("DesertTileset16x16\\Tileset16x16\\Mockup2.png"), (WIDTH - 200, HEIGHT)) # loads the background image with the function load_image, sets the dimensions of the bg to the WIDTH, and HEIGHT 
DESERT_WAYPOINTS = [(0, 318), (187, 318), (187, 468), (361, 468), (361, 544), (662, 545)]
DESERT_MAP = Map("Desert Map", WIDTH - 200, HEIGHT, DESERT_BACKGROUND, DESERT_WAYPOINTS) # creates a new Map object with the dimensions of the screen

GRASS_BACKGROUND = pygame.transform.scale(load_image("grass_map.png"), (WIDTH - 200, HEIGHT))
GRASS_WAYPOINTS = [(110, 600), (110, 401), (336, 401), (336, 271), (116, 271), (116, 147), (431, 147), (431, 330), (686, 330), (686, 518), (468, 518), (468, 600)]
GRASS_MAP = Map("Grass Map", WIDTH - 200, HEIGHT, GRASS_BACKGROUND, GRASS_WAYPOINTS)

# Styling
DEFAULTBUTTONSTYLE = Style(font_size=18)
DEFAULTBUTTONHOVERSTYLE = Style(font_size=18, background=(225, 225, 225))

class MainMenu:
    def __init__(self):
        # Display Variables
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.settings = {"hp": 150, "startingMoney": 200, "map": GRASS_MAP, "difficulty": "Medium"}

        # User Interface Variables
        self.menuInterface = Root(self.screen, width = WIDTH, height = HEIGHT)
        self.bg = UIElement(self.menuInterface, width=WIDTH, height=HEIGHT, defaultStyle=Style(background=(255, 255, 255)))

        # Main Menu Page
        self.mainMenuPage = Img(self.menuInterface, self.settings["map"].image, 0, 0, width=WIDTH, height=HEIGHT, defaultStyle=Style(opacity=100)) # Make these pages images
        self.mainTitle = Text(self.mainMenuPage, x=50, y=75, width=WIDTH, height=HEIGHT, text="Tower Defense", dropshadow=True, defaultStyle=Style(colour=(255, 255, 255), font_size=64, opacity=255))
        self.mainTitle.dock_x("center")

        self.startButton = UIElement(self.mainMenuPage, 400, 200, 100, 50, "Start", defaultStyle=DEFAULTBUTTONSTYLE, hoverStyle=DEFAULTBUTTONHOVERSTYLE, callback=self.start)
        self.startButton.dock_x("center")

        self.optionsButton = UIElement(self.mainMenuPage, 400, 300, 100, 50, "Options", defaultStyle=DEFAULTBUTTONSTYLE, hoverStyle=DEFAULTBUTTONHOVERSTYLE, callback=self.switch_to_options)
        self.optionsButton.dock_x("center")

        self.exitButton = UIElement(self.mainMenuPage, 400, 400, 100, 50, "Exit", defaultStyle=DEFAULTBUTTONSTYLE, hoverStyle=DEFAULTBUTTONHOVERSTYLE, callback=self.exit)
        self.exitButton.dock_x("center")

        # Options Page
        self.optionsMenuPage = Img(self.menuInterface, self.settings["map"].image, 0, 0, width=WIDTH, height=HEIGHT, defaultStyle=Style(opacity=100))
        self.optionsTitle = Text(self.optionsMenuPage, x=50, y=75, width=WIDTH, height=HEIGHT, text="Options", dropshadow=True, defaultStyle=Style(colour=(255, 255, 255), font_size=64, opacity=255))
        self.optionsTitle.dock_x("center")

        self.optionsReturnText = Text(self.optionsMenuPage, 20, 20, 20, 20, text='Press "Backspace" To Go Back',dropshadow=True, defaultStyle=Style(colour=(255, 255, 255), font_size=24, opacity=255))
        self.optionsReturnText.dock_x("left")

        self.optionsEasyButton = UIElement(self.optionsMenuPage, 200, 200, 100, 50, "Easy", defaultStyle=DEFAULTBUTTONSTYLE, hoverStyle=DEFAULTBUTTONSTYLE, callback=lambda: self.change_difficulty("Easy"))
        self.optionsMediumButton = UIElement(self.optionsMenuPage, 450, 200, 100, 50, "Medium", defaultStyle=DEFAULTBUTTONSTYLE, hoverStyle=DEFAULTBUTTONSTYLE, callback=lambda: self.change_difficulty("Medium"))
        self.optionsHardButton = UIElement(self.optionsMenuPage, 700, 200, 100, 50, "Hard", defaultStyle=DEFAULTBUTTONSTYLE, hoverStyle=DEFAULTBUTTONSTYLE, callback=lambda: self.change_difficulty("Hard"))

        self.optionsDesertMap = UIElement(self.optionsMenuPage, 300, 325, 150, 50, "Select Desert Map", defaultStyle=DEFAULTBUTTONSTYLE, hoverStyle=DEFAULTBUTTONSTYLE, callback=lambda: self.change_map("desert"))
        self.optionsGrassMap = UIElement(self.optionsMenuPage, 575, 325, 150, 50, "Select Grass Map", defaultStyle=DEFAULTBUTTONSTYLE, hoverStyle=DEFAULTBUTTONSTYLE, callback=lambda: self.change_map("grass"))

        self.optionsCurrentMap = Text(self.optionsMenuPage, x=50, y=450, width=WIDTH, height=HEIGHT, text=f"Current Map: {self.settings["map"].name}", dropshadow=True, defaultStyle=Style(colour=(255, 255, 255), font_size=32, opacity=255))
        self.optionsCurrentDifficulty = Text(self.optionsMenuPage, x=700, y=500, width=WIDTH, height=HEIGHT, text=f"Current Difficulty: {self.settings["difficulty"]}", dropshadow=True, defaultStyle=Style(colour=(255, 255, 255), font_size=32, opacity=255))
        self.optionsCurrentMap.dock_x("center")
        self.optionsCurrentDifficulty.dock_x("center")

        self.optionsMenuPage.set_visibility(False)

    def return_to_main_menu(self):
        self.switch_page("main")

    def change_difficulty(self, difficulty):
        self.settings["difficulty"] = difficulty

        if difficulty == "Easy":
            self.settings["hp"] = 200
            self.settings["startingMoney"] = 200
        elif difficulty == "Medium":
            self.settings["hp"] = 150
            self.settings["startingMoney"] = 200
        elif difficulty == "Hard":
            self.settings["hp"] = 100
            self.settings["startingMoney"] = 100

        self.optionsCurrentDifficulty.text=f"Current Difficulty: {self.settings["difficulty"]}"

    def change_map(self, map):

        if map == "grass":
            self.settings["map"] = GRASS_MAP
        elif map == "desert":
            self.settings["map"] = DESERT_MAP
            
        self.optionsMenuPage.image = self.settings["map"].image
        self.mainMenuPage.image = self.settings["map"].image
            
        self.optionsCurrentMap.text=f"Current Map: {self.settings["map"].name}"

    def switch_to_options(self):
        self.mainMenuPage.set_visibility(False)
        self.mainMenuPage.disabled = True
        self.optionsMenuPage.set_visibility(True)
        self.optionsMenuPage.disabled = False

    def switch_to_main(self):
        self.mainMenuPage.set_visibility(True)
        self.mainMenuPage.disabled = False
        self.optionsMenuPage.set_visibility(False)
        self.optionsMenuPage.disabled = True

    def start(self):
        Main(self.screen, self.settings["hp"], self.settings["startingMoney"], self.settings["map"]).run()

    def update(self):
        self.menuInterface.update(self.screen)

    def draw(self):
        self.screen.fill((0, 0, 0))

        self.menuInterface.render(self.screen)
        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.exit()
                    if event.key == pygame.K_0:
                        self.switch_page("main")
                    if event.key == pygame.K_BACKSPACE:
                        if self.optionsMenuPage.visible == True:
                            self.switch_to_main()
                self.menuInterface.handle_event(event)

            self.draw()
            self.update()

    def exit(self):
        pygame.quit()
        sys.exit()

class Main:
    def __init__(self, screen, hp=100, money=200, map=DESERT_MAP):
        # Display Variables
        self.screen = screen
        self.clock = pygame.time.Clock()

        # User Interface Variables
        self.userInterface = Root(self.screen, width = WIDTH, height = HEIGHT)
        self.sideMenu = UIElement(parent=self.userInterface, x=800, y=0, width=200, height=HEIGHT, defaultStyle=Style(background=(255, 255, 255)))

        styleDetails = Style(font_size=24)
        startWaveStyle = Style(font_size=48, colour=(255, 255, 255))
        insufficientFundsStyle = Style(font_size=48, colour=(255, 0, 0))
        
        self.waveText = Text(self.sideMenu, 0, 40, 200, 20,  text="Wave: //", defaultStyle=styleDetails)
        self.waveText.dock_x("center")

        self.healthText = Text(self.sideMenu, 0, 100, 200, 20, text="Health: //", defaultStyle=styleDetails)
        self.healthText.dock_x("center")

        self.moneyText =  Text(self.sideMenu, 0, 160, 200, 20, text="Money: //", defaultStyle=styleDetails)
        self.moneyText.dock_x("center")

        self.bar = Text(self.sideMenu, 0, 200, 200, 20, text="--------------------------------------------------------", defaultStyle=styleDetails)

        self.startWaveText = Text(self.userInterface, 75, 280, 200, 15, text="Press \"Space\" key to start the next wave", defaultStyle=startWaveStyle, dropshadow=True)
        self.insufficientFundsText = Text(self.userInterface, 250, 280, 200, 15, text="Insufficient Funds", defaultStyle=insufficientFundsStyle, dropshadow=True, canAlert=True)

        self.spawnTowerOne = UIElement(self.sideMenu, 30, 320, 50, 50, "Tower One", Style(background=(255, 255, 0)), callback=lambda: pygame.event.post(pygame.event.Event(SPAWN_TOWER_ONE)))
        self.spawnTowerTwo = UIElement(self.sideMenu, 120, 320, 50, 50, "Tower Two", Style(background=(255, 255, 0)), callback=lambda: pygame.event.post(pygame.event.Event(SPAWN_TOWER_TWO)))
        self.spawnTowerThree = UIElement(self.sideMenu, 30, 400, 50, 50, "Tower Three", Style(background=(255, 255, 0)), callback=lambda: pygame.event.post(pygame.event.Event(SPAWN_TOWER_THREE)))
        self.spawnTowerFour = UIElement(self.sideMenu, 120, 400, 50, 50, "Tower Four", Style(background=(255, 255, 0)), callback=lambda: pygame.event.post(pygame.event.Event(SPAWN_TOWER_FOUR)))

        # Pause Interface Variables
        self.pauseMenu = UIElement(parent=self.userInterface, x=0, y=0, width=800, height=600, defaultStyle=Style(background=(255, 255, 255), opacity=50))

        self.pauseMenuText = Text(self.pauseMenu, 40, 40, 400, 400, text="PAUSED", defaultStyle=startWaveStyle, dropshadow=True)
        self.pauseMenuText.dock_x("center")

        self.pauseMenuExitButton = UIElement(self.pauseMenu, 200, 250, 200, 50, "Exit To Main Menu", defaultStyle=DEFAULTBUTTONSTYLE, hoverStyle=DEFAULTBUTTONSTYLE, callback=self.pause_exit)
        self.pauseMenuExitButton.dock_x("center")
        self.pauseMenuExitButton = UIElement(self.pauseMenu, 200, 350, 200, 50, "Quit Game", defaultStyle=DEFAULTBUTTONSTYLE, hoverStyle=DEFAULTBUTTONSTYLE, callback=self.pause_exit_game)
        self.pauseMenuExitButton.dock_x("center")

        self.pauseMenu.set_visibility(False)
        self.pauseMenu.disabled = True

        # Game Variables
        self.hp = hp
        self.money = money
        self.running = True
        self.state = "running"

        # Map Variables
        self.selected_map = map.copy()

        # Tower Variables
        self.towers = [] # creates a list of Tower objects / (could extend this later and make a more in depth list of different towers)
        self.holdingTower = False
        self.currentTower = None

        # Wave System 
        self.waves = WaveSystem(ENEMY_ONE, ENEMY_TWO)

        self.testwaypoints = []

    def handle_event(self):
        for event in pygame.event.get(): # for loop of game event cycle
            if event.type == pygame.QUIT: # allows for QUITTING of game
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.waves.wave_running == False:
                    pygame.event.post(pygame.event.Event(START_WAVE))
                if event.key == pygame.K_q:
                    self.towers.clear()
                    self.waves.enemies.clear()
                if event.key == pygame.K_ESCAPE:
                    self.state = "paused"
                if event.key == pygame.K_p:
                    self.testwaypoints.append(pygame.mouse.get_pos())
                    print(self.testwaypoints)
            
            if event.type == START_WAVE:
                self.waves.start_wave(SPAWN_ENEMY)
            if event.type == SPAWN_ENEMY:
                self.waves.spawn_enemy(self.selected_map.waypoints)
            if event.type == END_WAVE:
                self.money += self.waves.end_wave(SPAWN_ENEMY)

            if event.type == SPAWN_TOWER_ONE:
                if self.holdingTower == False:
                    if TOWER_ONE.cost <= self.money:
                        self.currentTower = TOWER_ONE.copy()
                        self.towers.append(self.currentTower)
                        self.holdingTower = True
                    else:
                        self.insufficientFundsText.set_alert(True)
                    
            if event.type == SPAWN_TOWER_TWO:
                if self.holdingTower == False:
                    if TOWER_TWO.cost <= self.money:
                        self.currentTower = TOWER_TWO.copy()
                        self.towers.append(self.currentTower)
                        self.holdingTower = True
                    else:
                        self.insufficientFundsText.set_alert(True)
                    
            if event.type == SPAWN_TOWER_THREE:
                if self.holdingTower == False:
                    if TOWER_THREE.cost <= self.money:
                        self.currentTower = TOWER_THREE.copy()
                        self.towers.append(self.currentTower)
                        self.holdingTower = True
                    else:
                        self.insufficientFundsText.set_alert(True)
                    
            if event.type == SPAWN_TOWER_FOUR:
                if self.holdingTower == False:
                    if TOWER_FOUR.cost <= self.money:
                        self.currentTower = TOWER_FOUR.copy()
                        self.towers.append(self.currentTower)
                        self.holdingTower = True
                    else:
                        self.insufficientFundsText.set_alert(True)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.holdingTower == True and self.money < self.currentTower.cost:
                    self.holdingTower = False
                    self.currentTower = None
                    self.towers.pop()
                             
            if event.type == pygame.MOUSEBUTTONUP: # GETS THE MOST RECENT CREATED TOWER AND PLACES IT
                if event.button == 1 and len(self.towers) != 0 and self.money >= self.currentTower.cost and self.holdingTower: 
                    self.towers[-1].isPlaced = True
                    self.money -= self.currentTower.cost
                    self.moneyText.text = (f"Money: {str(self.money)}")
                    self.holdingTower = False

            self.userInterface.handle_event(event)

    def draw(self):
        self.selected_map.draw(self.screen)

        for tower in self.towers:
            tower.draw(self.screen)

        self.waves.draw(self.screen)
        self.userInterface.render(self.screen)
        pygame.display.flip()

    def update(self):
        for tower in self.towers:
            if self.holdingTower == False and tower.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                tower.drawRange = True
            else:
                tower.drawRange = False
                
            if tower.isPlaced and len(self.waves.enemies) != 0:
                tower.update(self.waves.enemies)

            elif tower.isPlaced and len(self.waves.enemies) == 0:
                tower.bullets.clear() # FIXED THIS ERROR OF BULLET LIST RETAINNIG POSITION ON ENEMY DEATHS

        if self.holdingTower == True:
            self.currentTower.move()

        self.userInterface.update(self.screen)
        self.money, self.hp = self.waves.update(SPAWN_ENEMY, END_WAVE, self.money, self.selected_map.waypoints, self.hp)

    def text_update(self):
        # Check Text States
        if self.waves.wave_running != True and self.insufficientFundsText.isAlerting != True:
            self.startWaveText.visible = True
        else:
            self.startWaveText.visible = False
                
        self.waveText.text = f"Wave: {self.waves.wave}"
        self.healthText.text = f"Health: {self.hp}"
        self.moneyText.text = f"Money: {str(self.money)}"

    def run(self):
        while self.running:
            self.clock.tick(60)
            if self.state == "paused":
                self.sideMenu.disabled = True
                self.pauseMenu.set_visibility(True)
                self.pauseMenu.disabled = False
 
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: # allows for QUITTING of game
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.state = "running"
                            self.sideMenu.disabled = False
                            self.pauseMenu.set_visibility(False)
                            self.pauseMenu.disabled = True
                    self.userInterface.handle_event(event)

                self.userInterface.update(self.screen)
                self.draw()
            if self.state == "running":
                self.handle_event()
                self.update()
                self.text_update()
                self.draw()

                if self.hp <= 0:
                    self.running = False
            if self.state == "exit":
                break

    def pause_exit(self):
        self.state = "exit"

    def pause_exit_game(self):
        pygame.quit()
        sys.exit()
            

if __name__ == "__main__":
    start = MainMenu()
    start.run()