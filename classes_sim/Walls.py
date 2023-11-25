import random
import pygame
import math


def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return int(math.floor(n * multiplier + 0.5) / multiplier)


class Walls:
    def __init__(self, screen_s, zoom, extra_map):
        self.TILE_SIZE = 50 * zoom
        self.COLOR = "blue"
        self.WALL_THICKNESS = 3 * zoom
        self.EXTRA_MAP = extra_map * zoom

        self.size = [self.round(screen_s[0]*self.EXTRA_MAP), self.round(screen_s[1]*self.EXTRA_MAP)]  # [w, h]
        self.screen_size = screen_s #[screen_s[0]*ZOOM, screen_s[1]*ZOOM]
        self.width_dif = self.round((self.size[0] - self.screen_size[0]) / 2)
        self.height_dif = self.round((self.size[1] - self.screen_size[1]) / 2)
        self.nots_w = round_half_up(self.size[0]/self.TILE_SIZE)
        self.nots_h = round_half_up(self.size[1]/self.TILE_SIZE)
        self.nots = self.create_nots()
        self.lines = self.create_maze()
        self.zoom = zoom
        self.create_walls()

    def round(self, value1):
        return round_half_up(value1 / self.TILE_SIZE) * self.TILE_SIZE

    def create_walls (self):

        top_wall = pygame.Rect((-self.width_dif, -self.height_dif), (self.size[0], self.WALL_THICKNESS))
        bottom_wall = pygame.Rect((-self.width_dif, self.size[1] - self.height_dif), (self.size[0] + self.WALL_THICKNESS, self.WALL_THICKNESS))
        left_wall = pygame.Rect((-self.width_dif, -self.height_dif), (self.WALL_THICKNESS, self.size[1] + self.WALL_THICKNESS))
        right_wall = pygame.Rect((self.size[0] - self.width_dif, -self.height_dif), (self.WALL_THICKNESS, self.size[1] + self.WALL_THICKNESS))

        self.lines.extend([top_wall, bottom_wall, right_wall, left_wall])
        #rect = pygame.Rect((con[0] * self.TILE_SIZE, con[1] * self.TILE_SIZE), (self.TILE_SIZE, self.WALL_THICKNESS))

    def create_nots(self):
        nots = []
        # for i in range(round_half_up(self.nots_w/self.EXTRA_MAP*(1-self.EXTRA_MAP)/2), round_half_up(self.nots_w+(self.nots_w/self.EXTRA_MAP*(1-self.EXTRA_MAP)/2))+1):
        #     for j in range(round_half_up(self.nots_h/self.EXTRA_MAP*(1-self.EXTRA_MAP)/2), self.nots_h+round_half_up(self.nots_h/self.EXTRA_MAP*(1-self.EXTRA_MAP)/2)+1):
        for i in range(round_half_up(-self.width_dif/self.TILE_SIZE)+1, round_half_up((self.size[0]-self.width_dif)/self.TILE_SIZE)):
            for j in range(round_half_up(-self.height_dif/self.TILE_SIZE)+1, round_half_up((self.size[1]-self.height_dif)/self.TILE_SIZE)):
                nots.append(Not([i,j]))


        return nots

    def create_maze(self):
        insaturated = []
        # for i in range(round_half_up(self.nots_w/self.EXTRA_MAP*(1-self.EXTRA_MAP)/2), round_half_up(self.nots_w+(self.nots_w/self.EXTRA_MAP*(1-self.EXTRA_MAP)/2))+1):
        #     for j in range(round_half_up(self.nots_h/self.EXTRA_MAP*(1-self.EXTRA_MAP)/2), self.nots_h+round_half_up(self.nots_h/self.EXTRA_MAP*(1-self.EXTRA_MAP)/2)+1):
        for i in range(round_half_up(-self.width_dif/self.TILE_SIZE)+1, round_half_up((self.size[0]-self.width_dif)/self.TILE_SIZE)):
            for j in range(round_half_up(-self.height_dif/self.TILE_SIZE)+1, round_half_up((self.size[1]-self.height_dif)/self.TILE_SIZE)):
                insaturated.append([i, j])  # [w, h]

        first = random.choice(insaturated)
        while len(insaturated) > 0:
            options_for_conn = []
            # for x in (range(-1, 2)):
            #     for y in (range(-1, 2)):
            #         if [first[0] + x, first[1] + y] in insaturated and [first[0] + x, first[1] + y] != first:
            #             options_for_conn.append([first[0] + x, first[1] + y])
            for i in range(-1, 2, 2):
                a = [first[0], first[1] + i]
                b = [first[0] + i, first[1]]
                if a in insaturated:
                    options_for_conn.append(a)
                if b in insaturated:
                    options_for_conn.append(b)


            insaturated.remove(first)

            if len(options_for_conn) > 0:
                second = random.choice(options_for_conn)
                for i in self.nots:
                    if i.index == first:
                        i.connection = second
                first = second
            else:
                if len(insaturated) > 0:
                    first = random.choice(insaturated)






                # # filter crosses
                # for i in self.nots:
                #     # dir_inf a esq_sup
                #     if con[0] == pos[0]+1 and con[1] == pos[1]-1:
                #
                #     # dir_sup a esq_inf
                #
                #     # esq_inf a dir_sup
                #
                #     # esq_sup a dir_inf
                #     pos = i.index
                #     con = i.connection
                #
                #     if (pos[0] == pos2[0] and pos1[1] < pos2[1]) and (con1[0] == con2[0] and con[1] > con2[1])


        lines = []
        for i in self.nots:
            pos = i.index
            con = i.connection
            if con != []:
                if pos[0] == con[0]: #vertical
                    if pos[1] < con[1]:
                        rect = pygame.Rect((pos[0] * self.TILE_SIZE, pos[1] * self.TILE_SIZE), (self.WALL_THICKNESS, self.TILE_SIZE+self.WALL_THICKNESS))
                    elif pos[1] > con[1]:
                        rect = pygame.Rect((con[0] * self.TILE_SIZE, con[1] * self.TILE_SIZE), (self.WALL_THICKNESS, self.TILE_SIZE+self.WALL_THICKNESS))
                elif pos[1] == con[1]: #horizontal
                    if pos[0] < con[0]:
                        rect = pygame.Rect((pos[0] * self.TILE_SIZE, pos[1] * self.TILE_SIZE), (self.TILE_SIZE+self.WALL_THICKNESS, self.WALL_THICKNESS))
                    elif pos[0] > con[0]:
                        rect = pygame.Rect((con[0] * self.TILE_SIZE, con[1] * self.TILE_SIZE), (self.TILE_SIZE+self.WALL_THICKNESS, self.WALL_THICKNESS))

                lines.append(rect)

                #lines.append(Line([pos[0] * self.TILE_SIZE, pos[1] * self.TILE_SIZE], [con[0] * self.TILE_SIZE, con[1] * self.TILE_SIZE]))

        return lines


    def draw(self, screen):
        for i in self.lines:
            pygame.draw.rect(screen, self.COLOR, i)


    def move(self, movement):
        for i in self.lines:
            i.move_ip(movement[0], movement[1])


class Not:
    def __init__(self, index):
        self.connection = []
        self.index = index

class Line:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop