from classes_network.Neuron import Neuron
import random


class Individual:
    def __init__(self, ID, receptors):
        self.ID = ID
        self.neurons = {}  # {"ID":neuron}
        self.receptors = receptors
        self.effectors = {"up": False, "down": False, "left": False, "right": False}
        self.max = 1
        self.min = -1
        self.first_neurons = {}  # {"ID":neuron}
        self.first_neuron_depolarization = 1
        self.creation_ratio = 10
        self.score = 0
        self.distance_travelled = 0



        self.create_neurons()

    def create_neurons(self):

        counter = len(self.receptors) #amount of colors -> number of first neurons
        gen_amount = [counter]
        counter = int(counter / self.creation_ratio)
        while counter > len(self.effectors):
            gen_amount.append(counter)
            counter = int(counter / self.creation_ratio)

        gen_amount.reverse()

        ID_counter = 0
        first_gen = [i for i in self.effectors]

        random.shuffle(first_gen)
        random_counter = 0
        for i in range(gen_amount[0]):
            if random_counter > len(first_gen) - 1:
                random.shuffle(first_gen)
                random_counter = 0

            self.neurons[str(ID_counter)] = Neuron(str(ID_counter), first_gen[random_counter])
            ID_counter += 1
            random_counter += 1

        next_gen = []
        for i in self.neurons:
            next_gen.append(self.neurons[i])

        random.shuffle(next_gen)
        random_counter = 0

        for i in gen_amount[1:]:
            next_gen_changing = []
            for j in range(i):
                if random_counter > len(next_gen) - 1:
                    random.shuffle(next_gen)
                    random_counter = 0
                neuron = Neuron(str(ID_counter), next_gen[random_counter])
                self.neurons[str(ID_counter)] = neuron
                next_gen_changing.append(neuron)
                ID_counter += 1
                random_counter += 1
            next_gen = next_gen_changing


        random.shuffle(next_gen)
        random_counter = 0
        for i in range(int(len(self.receptors))):
            if random_counter > len(next_gen) - 1:
                random.shuffle(next_gen)
                random_counter = 0
            self.first_neurons[str(i) + "_blue"] = Neuron(str(i) + "_blue", next_gen[random_counter])
            self.first_neurons[str(i) + "_white"] = Neuron(str(i) + "_white", next_gen[random_counter])
            self.first_neurons[str(i) + "_green"] = Neuron(str(i) + "_green", next_gen[random_counter])
            self.first_neurons[str(i) + "_yellow"] = Neuron(str(i) + "_yellow", next_gen[random_counter])
            self.first_neurons[str(i) + "_black"] = Neuron(str(i) + "_black", next_gen[random_counter])
            random_counter+=1

    def activate_first_neurons(self):
        for i in self.first_neurons:
            if self.first_neurons[i].is_activated:
                self.first_neurons[i].is_activated = False
        for square in range(len(self.receptors)):
            if self.receptors[square].changed:
                self.receptors[square].changed = False
                #print("called activate")
                self.first_neurons[str(square) + "_" + self.receptors[square].color].to.activate(self.first_neuron_depolarization)
                self.first_neurons[str(square) + "_" + self.receptors[square].color].is_activated = True


    def depolarize_neurons(self):
        for i in self.neurons:
            self.neurons[i].depolarize()


    def manage_activated_neurons(self, body, effectors):
        for i in self.neurons:
            self.neurons[i].manage_activated(body, effectors)

    def depolarize_effectors(self):
        for i in self.effectors:
            self.effectors[i] = False