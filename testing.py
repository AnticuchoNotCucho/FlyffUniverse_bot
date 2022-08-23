import cv2
import numpy as np
import pygame
import sys
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pygame import gfxdraw

np.set_printoptions(threshold=sys.maxsize)

# pygame setup
pygame.init()
screen = pygame.display.set_mode((700, 524))
pygame.display.set_caption("Pathfinding")
clock = pygame.time.Clock()


class Pathfinder:
    def __init__(self, matrix):
        self.matrix = matrix
        self.grid = Grid(matrix=matrix)
        self.select_surf = pygame.image.load("FlarisMap.jpg").convert_alpha()

        # create path
        self.path = []
        # Icon
        self.image = pygame.sprite.GroupSingle(Image())

    def draw_active_cell(self):
        mouse_pos = pygame.mouse.get_pos()
        row = mouse_pos[1]
        col = mouse_pos[0]
        current_cell = self.matrix[row][col]
        if current_cell == 1:
            gfxdraw.pixel(screen, col, row, (255, 0, 0))

    def create_path(self):

        # start
        # remember rows are Y and cols are X (inverted axis)
        start_x, start_y = self.image.sprite.get_coord()
        start = self.grid.node(start_x, start_y)
        # end
        mouse_pos = pygame.mouse.get_pos()
        end = self.grid.node(mouse_pos[0], mouse_pos[1])
        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        self.path, _ = finder.find_path(start, end, self.grid)
        self.grid.cleanup()
        self.image.sprite.set_path(self.path)
        print(self.path)

    def draw_path(self):
        if self.path:
            points = []
            for point in self.path:
                x = point[1]
                y = point[0]
                points.append((y, x))
            pygame.draw.lines(screen, (255, 0, 0), False, points, 2)

    def update(self):
        self.draw_active_cell()
        self.draw_path()

        # update Image
        self.image.update()
        self.image.draw(screen)


class Image(pygame.sprite.Sprite):
    def __init__(self):
        # basic
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("Nick.png").convert_alpha(), (10, 10))
        self.rect = self.image.get_rect(center=(220, 428))

        # movement
        self.pos = self.rect.center
        self.speed = 0.1
        self.direction = pygame.math.Vector2(0, 0)

        # path
        self.path = []
        self.collision_rects = []

    def get_coord(self):
        col = self.rect.centerx
        row = self.rect.centery
        return col, row

    def set_path(self, path):
        self.path = path
        self.create_collision_rects()
        self.get_direction()

    def create_collision_rects(self):
        if self.path:
            self.collision_rects = []
            for point in self.path:
                y = point[1]
                x = point[0]
                self.collision_rects.append(pygame.Rect(x, y, 10, 10))

    def get_direction(self):
        if self.collision_rects:
            start = pygame.math.Vector2(self.pos)
            end = pygame.math.Vector2(self.collision_rects[0].center)
            self.direction = (end - start).normalize()
            print(self.direction)
            print(start, end)
            print('press W')
        else:
            self.direction = pygame.math.Vector2(0, 0)
            self.path = []

    def check_collision(self):
        if self.collision_rects:
            for rect in self.collision_rects:
                if self.rect.colliderect(rect):
                    del self.collision_rects[0]
                    self.get_direction()

    def update(self):
        self.pos += self.direction * self.speed
        self.check_collision()
        self.rect.center = self.pos


# game setup
bg_surf = pygame.image.load("pixil-frame-0.png").convert()
img = cv2.imread('pixil-frame-0.png', 0)
img //= 254  # Now the pixels have range [0, 1]
img_list = img.tolist()  # We have a list of lists of pixels
matrix = np.array(img_list)
pathfinder = Pathfinder(matrix)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pathfinder.create_path()
    screen.blit(bg_surf, (0, 0))
    pathfinder.update()
    pygame.display.update()
    clock.tick(60)
