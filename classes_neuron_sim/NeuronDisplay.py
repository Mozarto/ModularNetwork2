

class NeuronDisplay:
    def __init__(self, pos, radius, itself):
        self.pos = pos
        self.radius = radius
        self.itself = itself
        self.line_to_distal_pos = []
        self.color = ""
        if len(itself.ID.split("_")) > 1:
            self.color = itself.ID.split("_")[1]

    def move(self, movement):
        self.pos = (self.pos[0] + movement[0], self.pos[1] + movement[1])