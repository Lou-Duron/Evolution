import pygame
import numpy as np
pygame.init()
from UI import *
from objects import *

COLOR = COLOR()
FONT = FONT()

SCREEN_SIZE  = 700
FPS = 60

WORLD_SIZE = 700
STEPS = 1000
FOOD_NB = 1000
LACS_NB = 5
OBST_NB = 5

ORG_NB = 100
MAX_NRJ = 500
ORG_VISION = 10

pygame.display.set_caption('Evolution')
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
clock = pygame.time.Clock()
speed = Slider("FPS", FPS, 61, 5, 345)
sliders = [speed]
pause = False
game_over = False


def draw(world):
    screen.fill(COLOR.BK)
    # Draw food
    for food in world.food:
        pygame.draw.rect(screen, COLOR.FOOD, [food[0], food[1], 2, 2])
    # Draw lacs
    for lac in world.lacs:
        pygame.draw.rect(screen, COLOR.BLUE, [lac[0], lac[1], lac[2], lac[3]])
    # Draw Obstacles
    for obst in world.obst:
        pygame.draw.rect(screen, COLOR.ORANGE, [obst[0], obst[1], obst[2], obst[3]])
    # Draw organisms
    for org in world.org:
        pygame.draw.rect(screen, COLOR.PINK, [org.x, org.y, 2, 2])
    # Draw variables
    screen.blit(FONT.arial.render(f"FPS : {str(int(clock.get_fps()))}", 1, COLOR.ORANGE), (10, 1))
    screen.blit(FONT.arial.render(f"Steps : {str(world.steps)}", 1, COLOR.ORANGE), (10, 15))
    screen.blit(FONT.arial.render(f"Generation : {str(world.generation)}", 1, COLOR.ORANGE), (10, 25))
################################################################################################## 
genomes = np.zeros((ORG_NB))
world = World(WORLD_SIZE, STEPS, FOOD_NB, LACS_NB, OBST_NB,
              ORG_NB, MAX_NRJ, ORG_VISION, genomes)
##################################################################################################
def loop():
    world.update()
    draw(world)
##################################################################################################
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
       # Slider drag and drop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for s in sliders:
                if s.button_rect.collidepoint(pos):
                    s.hit = True
        elif event.type == pygame.MOUSEBUTTONUP:
            for s in sliders:
                s.hit = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
               pause = False
    
    loop()

    for s in sliders:
        if s.hit:
            s.move()
        s.draw(screen)
    if speed.val == 61:
        clock.tick(1000) # Max speed
    elif speed.val == 5:
        pause = True
        clock.tick(1000)    
    else: 
        clock.tick(speed.val)
    pygame.display.update()
pygame.quit()
quit()