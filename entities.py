import math
import pygame
import random
from utility import load_image

class Map():
    def __init__(self, name, width, height, image, waypoints):
        self.name = name
        self.width = width
        self.height = height
        self.image = image
        self.waypoints = waypoints

    def copy(self):
        return Map(self.name, self.width, self.height, self.image, self.waypoints)

    def draw(self, screen):
        screen.blit(self.image, (0, 0))

class Enemy():
    def __init__(self, x, y, hp, speed, images, money):
        self.id = 1
        self.x, self.y = x, y # starts td enemies at the beginning of the paths (Could start them at different locations later in development)
        self.speed = speed # speed that enemy travels (Depending on enemy type can change)
        self.waypoint_index = 0 # first waypoint
        self.images = images
        self.money = money
        self.maxGrade = 5
        self.grade = random.randint(1, self.maxGrade)
        self.hp = hp
        self.startingHp = self.hp
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.remove = False
        self.current_frame = 0  # current frame index
        self.animation_speed = 5  # speed of animation (change frames every n updates)
        self.animation_counter = 0  # counter to control animation speed
        self.isFacingLeft = False
        self.healthBarWidth = 50
        self.maxHealthBarWidth = self.healthBarWidth

    @property
    def rect(self):
        rect = self.images[self.current_frame].get_rect()
        rect.x = self.x - self.images[self.current_frame].get_width() // 2
        rect.y = self.y - self.images[self.current_frame].get_height() // 2
        return rect
        
    # Returns a copy of itself
    def copy(self, x, y):
        return Enemy(x, y, self.hp, self.speed, self.images, self.money)

    def takeDamage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.remove = True
        decrementMultiplier = self.startingHp / self.maxHealthBarWidth
        new_width = int(self.hp / decrementMultiplier)
        self.healthBarWidth = new_width


    def update(self, waypoints):
        target_x, target_y = waypoints[self.waypoint_index] # gets the index of the target waypoint
        dx = target_x - self.x 
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2) # uses pythagoras to calculate distance between the enemy and the waypoint

        if dx >= 0:
            self.isFacingLeft = False
        else:
            self.isFacingLeft = True

        if distance > self.speed: # moves the enemy to the waypoint a fraction of the distance if distance > self.speed
            dx /= distance
            dy /= distance
            self.x += dx * self.speed # normalizing the enemy movement enseures the enemy moves at a constant speed regardless of distance
            self.y += dy * self.speed
        else:
            self.waypoint_index += 1 
            if self.waypoint_index >= len(waypoints):
                self.waypoint_index = len(waypoints)

        self.animation_counter += 1 # increment the animation counter 
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.images)  # cycle through frames

    def draw(self, screen):
        sprite = pygame.transform.flip(self.images[self.current_frame], self.isFacingLeft, False)
        screen.blit(sprite, (self.x - sprite.get_width() // 2, self.y - sprite.get_height() // 2))

        # Health bar logic
        # health bar position relative to the enemy's position
        health_bar_x = self.x - (self.maxHealthBarWidth // 2)  # adjust the X position of the health bar
        health_bar_y = self.y - 28 # adjust the Y position of the health bar
        
        # red health bar background
        pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, self.maxHealthBarWidth, 7))
        
        # green health bar based on current health
        pygame.draw.rect(screen, (0, 128, 0), (health_bar_x, health_bar_y, self.healthBarWidth, 7))

class Tower:
    def __init__(self, x, y, images, bulletImages, cost=10, shoot_cooldown=10, dmgOvertime=0, bulletDmg=10, range=150): # initialises the tower object 
        self.x, self.y = x, y # the x and y coordinates 
        self.images = images
        self.bulletImages = bulletImages
        self.isPlaced = False # this checks whether the tower is placed, crucial for debugging and combat
        self.bullets = []
        self.shoot_cooldown = shoot_cooldown
        self.shoot_timer = 0
        self.cost = cost
        self.dmgOvertime = dmgOvertime
        self.bulletDmg = bulletDmg
        self.current_frame = 0  # Current frame index
        self.nearbyEnemies = []
        
        self.range = range
        self.range_surface = pygame.Surface((self.range * 2, self.range * 2), pygame.SRCALPHA)  # Create a transparent surface for the range circle
        self.drawRange = False
        # self.range_surface.fill((0, 0, 0, 50))  # Fill the surface with a semi-transparent blue color

    @property
    def rect(self):
        rect = self.images[self.current_frame].get_rect()
        rect.x = self.x - self.images[self.current_frame].get_width() // 2
        rect.y = self.y - self.images[self.current_frame].get_height() // 2
        return rect
    
    # Returns a copy of itself
    def copy(self):
        return Tower(self.x, self.y, self.images, self.bulletImages, self.cost, self.shoot_cooldown, self.dmgOvertime, self.bulletDmg, self.range)

    def draw_range(self, screen):
        pygame.draw.circle(screen, (0, 0, 0, 100), (self.x, self.y), self.range, 1)  # Draw a blue circle on the surface

    def get_distances(self, enemies):
        enemy_distances = {}
        for enemy in enemies:
            distance_to_enemy = math.sqrt((enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2)
            enemy_distances[enemy.id] = distance_to_enemy

        # Sorting the dictionary by values in ascending order
        sorted_enemy_distances = dict(sorted(enemy_distances.items(), key=lambda item: item[1]))
        return sorted_enemy_distances
    
    def match_enemy_distance(self, enemies, sorted_enemy_distances):
        for enemy in enemies:
            for id, distance in sorted_enemy_distances.items():
                if enemy.id == id:
                    return enemy, distance

    def shoot(self, enemies):
        if enemies != []:
            if self.shoot_timer <= 0:  # Check if tower can shoot based on cooldown
                sorted_enemy_distances = self.get_distances(enemies)
                enemy, distance = self.match_enemy_distance(enemies, sorted_enemy_distances)
                if distance <= self.range:  # Check if the enemy is within tower's range
                    bullet = Bullet(self.x, self.y, enemy, self.bulletImages, self.bulletDmg)
                    self.bullets.append(bullet)
                    self.shoot_timer = self.shoot_cooldown
                    # Animation logic 
                    self.current_frame = (self.current_frame + 1) % len(self.images)  # Cycle through frames

    def update_bullets(self):
        if self.shoot_timer > 0:
            self.shoot_timer -= 1  # Decrement shoot timer

        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.remove:
                self.bullets.remove(bullet)

    def draw_bullets(self, screen):
        for bullet in self.bullets:
            bullet.draw(screen)

    def draw(self, screen):
        self.draw_bullets(screen)
        screen.blit(self.images[self.current_frame], (self.x - self.images[self.current_frame].get_width() // 2, self.y - self.images[self.current_frame].get_height() // 2))         
        if self.drawRange == True:
            self.draw_range(screen)

    def move(self): # IF TOWER IS NOT PLACED IT WILL FOLLOW MOUSE || NEED TO ADD SELL SYSTEM 
        if self.isPlaced == False:
            mx, my = pygame.mouse.get_pos() # get the mouse position
            self.x = mx # mouse pos x
            self.y = my # mouse pos y

    def update(self, enemies):
        self.move()
        self.update_bullets()
        self.shoot(enemies)

class Bullet:
    def __init__(self, x, y, target, images, damage):
        self.x, self.y = x, y
        self.target = target
        self.speed = 5
        self.images = images
        self.damage = damage
        self.current_frame = 0  # Current frame index
        self.animation_speed = 5  # Speed of animation (change frames every n updates)
        self.animation_counter = 0  # Counter to control animation speed
        self.remove = False
        self.oldXCalculation = 0
        self.oldYCalculation = 0
        
    @property
    def rect(self):
        rect = self.images[self.current_frame].get_rect()
        rect.x = self.x - self.images[self.current_frame].get_width() // 2
        rect.y = self.y - self.images[self.current_frame].get_height() // 2
        return rect
    
    def update(self):
        if self.target.hp > 0:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            distance = math.sqrt(dx**2 + dy**2)

            if distance != 0:
                dx /= distance
                dy /= distance
                xCalculation = dx * self.speed
                yCalculation = dy * self.speed
                self.oldXCalculation = xCalculation
                self.oldYCalculation = yCalculation
                self.x += xCalculation
                self.y += yCalculation
                distance = math.sqrt(dx**2 + dy**2)
        else:
            self.x += self.oldXCalculation
            self.y += self.oldYCalculation


        # Animation logic
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.images)  # Cycle through frames

        self.applyDamage()

    def applyDamage(self):
        if self.rect.colliderect(self.target.rect) and self.target.hp > 0:
            self.target.takeDamage(self.damage)
            self.remove = True
        elif self.x > 800 or self.y > 600:
            self.remove = True
    
    def draw(self, screen):
        screen.blit(self.images[self.current_frame], (self.x - self.images[self.current_frame].get_width() // 2, self.y - self.images[self.current_frame].get_height() // 2))            

class WaveSystem:
    def __init__(self, *args):
        self.wave = 0
        self.wave_running = False
        self.enemies = []
        self.max_enemies = self.calculate_max_enemies()
        self.enemy_one = args[0]
        self.enemy_two = args[1]
        self.enemy_counter = 0
        self.removed_enemies = 0
        
    def start_wave(self, SPAWN_ENEMY):
        self.wave_running = True
        self.wave += 1
        self.max_enemies = self.calculate_max_enemies()
        pygame.time.set_timer(SPAWN_ENEMY, random.randrange(500, 1000))

    def end_wave(self, SPAWN_ENEMY):
        self.wave_running = False
        pygame.time.set_timer(SPAWN_ENEMY, 0)
        self.enemies = []
        self.removed_enemies = 0
        self.enemy_counter = 0
        waveCompletionBonus = self.max_enemies * 5

        return waveCompletionBonus
        
    def calculate_max_enemies(self):
        wave_calculation = int(0.5 * (self.wave + 4)**2 + 0.5 * (self.wave + 4))
        return random.randint(wave_calculation, wave_calculation + 2)
    
    def spawn_enemy(self, waypoints):
        if self.wave_running and self.enemy_counter < self.max_enemies:
            enemyChoice = random.randint(0, 1)  # Adjusted the range to match the number of enemy types
            if enemyChoice == 0:
                enemy = self.enemy_one.copy(waypoints[0][0], waypoints[0][1])
                enemy.id = self.enemy_counter + 1
                self.enemies.append(enemy)
            elif enemyChoice == 1:
                enemy = self.enemy_two.copy(waypoints[0][0], waypoints[0][1])
                enemy.id = self.enemy_counter + 1
                self.enemies.append(enemy)

            self.enemy_counter += 1

      
    def draw(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen) # calls the draw function from entities.py (using screen as a reference)
    
    def update(self, SPAWN_ENEMY, END_WAVE, money, waypoints, hp):
        if self.wave_running:     
            for enemy in self.enemies:
                enemy.update(waypoints) # calls the update function from entities.py

                if enemy.waypoint_index == len(waypoints): # Check if enemy reached the last waypoint
                    self.enemies.remove(enemy) # removes enemy from the list if it reaches the last waypoint
                    self.removed_enemies += 1
                    
                    hp -= 10 # enemy base damage == 10
                elif enemy.hp > 0:
                    pass
                elif enemy.remove == True:
                    money += enemy.money
                    self.enemies.remove(enemy) # removes enemy from the list if it has less than or equal to 0 health
                    self.removed_enemies += 1
                    
            if self.enemy_counter >= self.max_enemies:
                pygame.time.set_timer(SPAWN_ENEMY, 0)
                    
            if self.removed_enemies >= self.max_enemies and self.enemy_counter >= self.max_enemies:
                if self.wave_running:
                    pygame.event.post(pygame.event.Event(END_WAVE))
        return money, hp