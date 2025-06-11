import pygame
from config import CELL_SIZE, GRID_WIDTH, GRID_HEIGHT

class Creature:
    def __init__(self, name,lifespan, energy, speed, genome, vision_range, behaviors, x, y, age=0):
        self.name = name
        self.age = age
        self.lifespan = lifespan
        self.energy = energy
        self.speed = speed
        self.genome = genome
        self.vision_range = vision_range
        self.behaviors = behaviors
        self.is_alive = True
        self.cell_x = x
        self.cell_y = y
    
    def move(self, dx, dy):
        if self.energy > 0:
            self.cell_x += dx
            self.cell_y += dy
            self.energy -= 1 
    
    def decide_move(self, visible_environment):
        # Retourne un vecteur de mouvement ou une direction (dx, dy)
        pass
    
    def eat(self, resource):
        if resource:
            self.energy += resource.nutrition
            resource.consume()


    def reproduce(self):
        if self.energy > 30:
            child_genome = self.genome.copy()
            child_genome.mutate()
            self.energy -= 20
            stats = child_genome.to_stats()
            behaviors = child_genome.to_behavior()
            return Creature(name=self.name+"_child", age=0, lifespan=0, energy=stats["energy"], speed=stats["speed"], genome=child_genome, vision_range=stats["vision"], behaviors=behaviors, x=self.x+1, y=self.y)
        return None
    
    def die(self):
        self.is_alive = False

    def mutate(self):
        # Logic for mutating the creature's genome
        self.genome.mutate()
        
    def render(self, screen, camera_x, camera_y):
        color = self.genome.to_color()
        shape = self.genome.to_shape()

        screen_x = (self.cell_x - camera_x) * CELL_SIZE + CELL_SIZE // 2
        screen_y = (self.cell_y - camera_y) * CELL_SIZE + CELL_SIZE // 2

        if shape == 0:
            pygame.draw.circle(screen, color, (screen_x, screen_y), 10)
        elif shape == 1:
            pygame.draw.rect(screen, color, (screen_x - 10, screen_y - 10, 20, 20))
        elif shape == 2:
            pygame.draw.polygon(screen, color, [
                (screen_x, screen_y - 10),
                (screen_x - 10, screen_y + 10),
                (screen_x + 10, screen_y + 10)
            ])
    
    def interact(self, other_creature):
        if self.energy > 0 and other_creature.is_alive:
            # Logic for interaction (e.g., mating, fighting)
            pass
    
    def age_tick(self):
        self.age += 1
        self.energy -= 1
        if self.age > self.lifespan or self.energy <= 0:
            self.die()