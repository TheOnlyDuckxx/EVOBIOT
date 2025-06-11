import pygame
from random import *
from genome import Genome
from creature import Creature
from environment import Cellule
from config import GRID_WIDTH, GRID_HEIGHT, CELL_SIZE, VISIBLE_RADIUS

def create_life(name, x, y):
    genome = Genome()
    stats = genome.to_stats()
    behaviors = genome.to_behavior()
    return Creature(name=name, age=0, lifespan=100, energy=stats["energy"], speed=stats["speed"], genome=genome, vision_range=stats["vision"], behaviors=behaviors, x=x, y=y)

def draw_grid(screen, spacing=40, color=(200, 200, 200)):
    width, height = screen.get_size()
    for x in range(0, width, spacing):
        pygame.draw.line(screen, color, (x, 0), (x, height))
    for y in range(0, height, spacing):
        pygame.draw.line(screen, color, (0, y), (width, y))


def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("EVOBIOT")
    clock = pygame.time.Clock()
    running = True

    creatures = []
    for i in range(1):
        c = create_life(f"Creature_{i}", 2, 3)
        creatures.append(c)



    SEED = randint(0, 10000)

    environment_cache = {}
    camera_x, camera_y = 0, 0


    while running:
        screen.fill((255, 255, 255))
        for screen_y in range(GRID_HEIGHT):
            for screen_x in range(GRID_WIDTH):
                world_x = screen_x + camera_x
                world_y = screen_y + camera_y
                key = (world_x, world_y)

                if key not in environment_cache:
                    environment_cache[key] = Cellule(world_x, world_y, seed=SEED)
                
                cell = environment_cache[key]
                rect_x = screen_x * CELL_SIZE
                rect_y = screen_y * CELL_SIZE
                pygame.draw.rect(screen, cell.get_color(), (rect_x, rect_y, CELL_SIZE, CELL_SIZE))
        

        draw_grid(screen)

        to_delete = []
        for (x, y) in environment_cache:
            if abs(x - camera_x) > VISIBLE_RADIUS or abs(y - camera_y) > VISIBLE_RADIUS:
                to_delete.append((x, y))

        for key in to_delete:
            del environment_cache[key]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_LEFT:
                    camera_x -= 1
                elif event.key == pygame.K_RIGHT:
                    camera_x += 1
                elif event.key == pygame.K_UP:
                    camera_y -= 1
                elif event.key == pygame.K_DOWN:
                    camera_y += 1
        
        for creature in creatures:
            creature.render(screen, camera_x, camera_y)

        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()

if __name__ == "__main__":
    main()
