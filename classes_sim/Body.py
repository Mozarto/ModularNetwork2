import math

import pygame


class Body(pygame.Rect):
    def __init__(self, screen_s, zoom):
        self.COLOR = "white"
        self.SPEED = 0.3 * zoom
        self.INERTIA = 0.95
        self.SIZE = 10 * zoom

        self.initial_pos = (0,0)

        super().__init__([screen_s[0]/2, screen_s[1]/2], (self.SIZE, self.SIZE))
        self.speed_vector = [0, 0] #[x, y]
        self.score = 0

    def position(self, map, food):
        for i in map.lines:
            if self.colliderect(i):
                if i.size[0] > i.size[1]:
                    map.move([0, map.TILE_SIZE/2])
                    food.move([0, map.TILE_SIZE/2])
                else:
                    map.move([map.TILE_SIZE/2, 0])
                    food.move([map.TILE_SIZE/2, 0])
                self.initial_pos = (self.x, self.y)
                self.position(map, food)
        for i in food.trees:
            if self.colliderect(i):
                map.move([map.TILE_SIZE / 2, map.TILE_SIZE / 2])
                food.move([map.TILE_SIZE / 2, map.TILE_SIZE / 2])
                self.initial_pos = (self.x, self.y)
                self.position(map, food)

    def up(self):
        self.speed_vector[1] += self.SPEED

    def down(self):
        self.speed_vector[1] -= self.SPEED

    def left(self):
        self.speed_vector[0] += self.SPEED

    def right(self):
        self.speed_vector[0] -= self.SPEED

    def move_manager(self):
        self.speed_vector[0] *= self.INERTIA
        self.speed_vector[1] *= self.INERTIA

    def draw(self, screen):
        pygame.draw.rect(screen, self.COLOR, self)

    def calculate_distance_travelled(self):
        return math.sqrt(abs(self.x-self.initial_pos[0])**2 + abs(self.y-self.initial_pos[1])**2)

