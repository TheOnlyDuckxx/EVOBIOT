import pygame
from random import choice, random, randint
from config import CELL_SIZE, SEED
from environment import Cellule
from genome import Genome
import math

class Creature:
    _id_counter = 0  # pour debug/logs
    
    def __init__(self, name, energy, speed, genome, vision_range, behaviors, x, y, age=0):
        Creature._id_counter += 1
        self.id = Creature._id_counter

        self.name = name
        self.age = age
        self.energy = energy
        self.speed = speed
        self.genome = genome
        self.vision_range = vision_range
        self.behaviors = behaviors
        self.is_alive = True

        self.cell_x = x
        self.cell_y = y
        self.last_cell = None

        self.last_move_time = 0
        self.move_delay = int(30 - self.speed * 25)
        self.move_delay = max(self.move_delay, 2)

    def move(self, dx, dy):
        if self.energy > 0:
            self.last_cell = (self.cell_x, self.cell_y)
            self.cell_x += dx
            self.cell_y += dy
            self.energy -= 1

    def decide_move(self, visible_environment):
        best_score = -float('inf')
        best_dir = (0, 0)

        for (dx, dy), cell in visible_environment.items():
            if dx == 0 and dy == 0:
                continue

            score = 0
            if cell.cell_type == "nourriture":
                score += 100
            elif cell.cell_type == "sol":
                score += 5
            elif cell.cell_type == "arbre":
                score += 2
            elif cell.cell_type == "eau":
                score -= 100

            if (self.cell_x + dx, self.cell_y + dy) == self.last_cell:
                score -= 10

            score += self.behaviors["curiosity"] * 10
            score -= (abs(dx) + abs(dy)) * 2

            if score > best_score:
                best_score = score
                best_dir = (dx, dy)

        if best_score <= 0 or (best_score < 10 and random() < self.behaviors["curiosity"] + 0.1):
            return choice([(0, 1), (1, 0), (0, -1), (-1, 0)])

        dx, dy = best_dir
        return (dx // abs(dx) if dx else 0, dy // abs(dy) if dy else 0)

    def eat(self, cell):
        if cell.cell_type == "nourriture" and cell.active:
            self.energy += 20
            cell.active = False
            cell.cell_type = "sol"

    def reproduce(self, other):
        if self.energy > 30:
            data1 = self.genome.data
            data2 = other.genome.data

            # On calcule la moyenne (et on convertit en int si besoin)
            moyennes = [
                int((data1[i] + data2[i]) / 2)
                for i in range(len(data1))
            ]

            # On crée un véritable Genome à partir de ces données
            child_genome = Genome(data=moyennes)
            child_genome.mutate()
            self.energy -= 20

            stats = child_genome.to_stats()
            behaviors = child_genome.to_behavior()

            return Creature(
                name=self.name + "_child",
                age=0,
                lifespan=randint(500, 1500),
                energy=stats["energy"],
                speed=stats["speed"],
                genome=child_genome,
                vision_range=stats["vision"],
                behaviors=behaviors,
                x=self.cell_x + choice([-1, 1]),
                y=self.cell_y + choice([-1, 1])
            )
        return None

    def die(self):
        self.is_alive = False

    def mutate(self):
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
        if self.is_alive and other_creature.is_alive:
            if self.can_reproduce_with(other_creature):
                return self.reproduce(other_creature)
        return None

    @staticmethod
    def color_distance(c1, c2):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))

    def can_reproduce_with(self, other, color_threshold=80):
        # condition de proximité spatiale et d'énergie existante
        close_enough = (
            abs(self.cell_x - other.cell_x) <= 1 and
            abs(self.cell_y - other.cell_y) <= 1 and
            self.energy > 30 and
            other.energy > 30
        )

        if not close_enough:
            return False

        # on récupère les couleurs RGB
        c1 = self.genome.to_color()
        c2 = other.genome.to_color()

        # on vérifie que la distance de couleur est sous le seuil
        if Creature.color_distance(c1, c2) > color_threshold:
            return False

        return True

    def age_tick(self):
        self.age += 1
        self.energy -= 0.1
        if self.energy <= 0:
            self.die()

    def get_visible_cells(self, environment_cache):
        visible = {}
        for dy in range(-self.vision_range, self.vision_range + 1):
            for dx in range(-self.vision_range, self.vision_range + 1):
                tx = self.cell_x + dx
                ty = self.cell_y + dy
                key = (tx, ty)
                if key not in environment_cache:
                    environment_cache[key] = Cellule(tx, ty, seed=SEED)
                visible[(dx, dy)] = environment_cache[key]
        return visible

    def update(self, environment_cache, current_tick):
        self.age_tick()
        if not self.is_alive:
            return

        if current_tick - self.last_move_time >= self.move_delay:
            visible = self.get_visible_cells(environment_cache)
            dx, dy = self.decide_move(visible)
            self.move(dx, dy)
            self.last_move_time = current_tick

            current_key = (self.cell_x, self.cell_y)
            if current_key in environment_cache:
                self.eat(environment_cache[current_key])