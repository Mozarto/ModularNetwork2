import math

from classes_neuron_sim.NeuronDisplay import NeuronDisplay
import pygame

class ManageNeurons:
    def __init__(self, first_neurons, neurons, effectors):
        self.first_neurons = first_neurons
        self.first_neurons_display = {}
        self.neurons = neurons
        self.neurons_display = {}
        self.effectors = effectors

        self.neuron_radius = 1
        self.neuron_halo_radius = 2
        self.space_between_neurons = self.neuron_radius*16

        self.screen_movement_speed = 50

        self.effectors_pos = {"up": (0, 0), "down": (0, 0), "right": (0, 0), "left": (0, 0)}

        counter = 0
        for i in self.effectors_pos:
            counter += 1
            self.effectors_pos[i] = (math.ceil(8 + len(self.neurons) /
                                               (len(self.first_neurons) / 5)) * self.space_between_neurons,
                                     counter * self.space_between_neurons)


        self.create_neuronDisplay()

    def create_neuronDisplay(self):
        counter_v = 1
        counter_h = 1
        for i in self.first_neurons:
            self.first_neurons_display[self.first_neurons[i].ID] = NeuronDisplay((self.space_between_neurons*counter_h, self.space_between_neurons*counter_v),
                                                                                 self.neuron_radius, self.first_neurons[i])
            if counter_h == 5:
                counter_v += 1
                counter_h = 0
            counter_h +=1

        counter_v = 1
        counter_h = 1
        for i in self.neurons:
            self.neurons_display[self.neurons[i].ID] = NeuronDisplay((self.space_between_neurons*(counter_h+6), self.space_between_neurons*counter_v), self.neuron_radius, self.neurons[i])

            if counter_v == len(self.first_neurons)/5:
                counter_h += 1
                counter_v = 0
            counter_v += 1





    def draw(self, surface):
        for i in self.first_neurons_display:
            color = "grey45"
            if self.first_neurons_display[i].itself.is_activated:
                color = "lightgoldenrod"
                if type(self.first_neurons_display[i].itself.to) != str:
                    pygame.draw.line(surface, color, self.first_neurons_display[i].pos,
                                     self.neurons_display[self.first_neurons_display[i].itself.to.ID].pos)
                else:
                    pass

            pygame.draw.circle(surface, self.first_neurons_display[i].color, self.first_neurons_display[i].pos,
                               self.neuron_halo_radius)

            pygame.draw.circle(surface, color, self.first_neurons_display[i].pos,
                               self.first_neurons_display[i].radius)


        for i in self.neurons_display:
            color = "grey45"
            #print(self.neurons_display[i].itself.to + str(self.neurons_display[i].itself.is_activated)) if type(self.neurons_display[i].itself.to) == str else "."
            if self.neurons_display[i].itself.is_activated:
                color = "lightgoldenrod"
                if type(self.neurons_display[i].itself.to) != str:
                    pygame.draw.line(surface, color, self.neurons_display[i].pos,
                                 self.neurons_display[self.neurons_display[i].itself.to.ID].pos)
                else:
                    #print(self.effectors[self.neurons_display[i].itself.to])
                    pygame.draw.line(surface, color, self.neurons_display[i].pos,
                                     self.effectors_pos[self.neurons_display[i].itself.to])

            pygame.draw.circle(surface, color, self.neurons_display[i].pos,
                               self.neurons_display[i].radius)

        counter = 0
        for i in self.effectors:
            counter += 1
            color = "salmon"

            if self.effectors[i]:
                color = "tan"

            pygame.draw.circle(surface, color, self.effectors_pos[i], self.neuron_radius)



    def move(self):
        def movement(mov):
            for i in self.first_neurons_display:
                self.first_neurons_display[i].move(mov)
            for i in self.neurons_display:
                self.neurons_display[i].move(mov)
            for i in self.effectors_pos:
                self.effectors_pos[i] = (self.effectors_pos[i][0] + mov[0], self.effectors_pos[i][1] + mov[1])

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            movement((0, self.screen_movement_speed))
        if keys[pygame.K_s]:
            movement((0, -self.screen_movement_speed))
        if keys[pygame.K_a]:
            movement((-self.screen_movement_speed, 0))
        if keys[pygame.K_d]:
            movement((self.screen_movement_speed, 0))


