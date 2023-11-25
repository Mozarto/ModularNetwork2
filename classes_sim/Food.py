import pygame
import random


class Food:
    def __init__(self, map, zoom, food_timer, food_density):
        self.COLOR = "yellow"
        self.DENSITY_REG = 100000*zoom**2
        self.TIMER_LIMIT = 600
        self.MAX_FOOD_INCREASE = 5

        self.zoom = zoom
        self.trees = self.create_trees(map)


    def get_foods(self):
        foods = []
        for tree in self.trees:
            foods += tree.foods
        return foods


    def create_trees(self, map):
        trees = []
        for i in range(int(map.size[0]*map.size[1]/self.DENSITY_REG)):
            trees.append(Trees([random.randint(-map.width_dif, map.size[0]-map.width_dif), random.randint(-map.height_dif, map.size[1]-map.height_dif)], self.zoom))
        #print(len(trees))
        return trees

    def draw(self, screen, map):
        if len(self.trees) > 0:
            for i in self.trees:
                pygame.draw.rect(screen, self.COLOR, i)
                i.draw_food(screen)

    def create_foods_timer(self):
        if len(self.trees) > 0:
            for i in self.trees:
                i.food_timer += random.randint(0, self.MAX_FOOD_INCREASE)
                if i.food_timer > self.TIMER_LIMIT:
                    i.food_timer = 0
                    i.create_foods()

    def move(self,movement):
        for tree in self.trees:
            tree.move_ip(movement[0], movement[1])
            for food in tree.foods:
                food.move_ip(movement[0], movement[1])


class Trees(pygame.Rect):
    def __init__(self, pos, zoom):
        self.SIZE = 15 * zoom
        self.FOOD_SIZE = 5 * zoom
        self.RANGE = 30 * zoom
        self.FOOD_COLOR = "green"

        super().__init__(pos, [self.SIZE, self.SIZE])
        self.foods = []
        self.food_timer = 0

    def create_foods(self):
        if len(self.foods) < 5:
            self.foods.append(pygame.Rect([random.randint(self.x-self.RANGE, self.x+self.RANGE),
                                       random.randint(self.y-self.RANGE, self.y+self.RANGE)], [self.FOOD_SIZE, self.FOOD_SIZE]))


    def draw_food(self, screen):
        for i in self.foods:
            pygame.draw.rect(screen, self.FOOD_COLOR, i)
