import pygame


class View:
    def __init__(self, size, square):
        self.size = size
        self.square_size = (square, square)
        self.squares = []
        for x in range(int(size[0]/self.square_size[0])):
            for y in range(int(size[1]/self.square_size[1])):
                self.squares.append(Square((x*self.square_size[0], y*self.square_size[1]), self.square_size))

        #print(len(self.squares))

    def check(self, lists, colors):
        for square in self.squares:
            counter = 0
            for i in range(len(lists)):
                indices = square.collidelistall(lists[i])

                if len(indices) > 0:
                    counter += 1
                    if square.color != colors[i]:
                        square.color = colors[i]
                        square.changed = True

            if counter == 0:
                if square.color != "black":
                    square.color = "black"
                    square.changed = True

    def draw(self, surface):
        for square in self.squares:
            pygame.draw.rect(surface, square.color, square)




class Square(pygame.Rect):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.color = "black"
        self.changed = True