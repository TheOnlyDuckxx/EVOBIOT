import pygame
from random import choice
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
        self.last_move_time = 0
        self.move_delay = int(20 - self.speed * 16)
        self.move_delay = max(self.move_delay, 1)  # sécurité

    
    def move(self, dx, dy):
        if self.energy > 0:
            self.cell_x += dx
            self.cell_y += dy
            self.energy -= 0.2 
    
    def decide_move(self, visible_environment):
        best_score = -float('inf')
        best_dir = (0, 0)

        for (dx, dy), cell in visible_environment.items():
            if dx == 0 and dy == 0:
                continue  # on ignore la cellule actuelle

            score = 0
            if cell.cell_type == "nourriture":
                score += 100
            elif cell.cell_type == "sol":
                score += 5
            elif cell.cell_type == "arbre":
                score += 2
            elif cell.cell_type == "eau":
                score -= 100  # interdit

            # Influencé par les traits comportementaux
            score += self.behaviors["curiosity"] * 10
            score -= (abs(dx) + abs(dy)) * 2  # plus loin = moins intéressant

            if score > best_score:
                best_score = score
                best_dir = (dx, dy)

        if best_score <= 0:
            # Mouvement aléatoire
            return choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
        # Normaliser à une seule case de mouvement
        dx, dy = best_dir
        if dx != 0:
            dx = dx // abs(dx)
        if dy != 0:
            dy = dy // abs(dy)
        return dx, dy
    
    def eat(self, cell):
        if cell.cell_type == "nourriture" and cell.active:
            self.energy += 20
            cell.active = False
            cell.cell_type = "sol"


    def reproduce(self):
        if self.energy > 30:
            child_genome = self.genome.copy()
            child_genome.mutate()
            self.energy -= 20
            stats = child_genome.to_stats()
            behaviors = child_genome.to_behavior()
            return Creature(
                name=self.name + "_child",
                age=0,
                lifespan=0,
                energy=stats["energy"],
                speed=stats["speed"],
                genome=child_genome,
                vision_range=stats["vision"],
                behaviors=behaviors,
                x=self.cell_x + 1,
                y=self.cell_y
            )
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
    
    def get_visible_cells(self, environment_cache):
        visible = {}
        for dy in range(-self.vision_range, self.vision_range + 1):
            for dx in range(-self.vision_range, self.vision_range + 1):
                tx = self.cell_x + dx
                ty = self.cell_y + dy
                key = (tx, ty)
                if key in environment_cache:
                    visible[(dx, dy)] = environment_cache[key]
        return visible

    
    def update(self, environment_cache, current_tick):
        self.age_tick()

        # Déplacement
        if current_tick - self.last_move_time >= self.move_delay:
            visible = self.get_visible_cells(environment_cache)
            dx, dy = self.decide_move(visible)
            self.move(dx, dy)
            self.last_move_time = current_tick

            # Position actuelle
            current_key = (self.cell_x, self.cell_y)
            if current_key in environment_cache:
                self.eat(environment_cache[current_key])

