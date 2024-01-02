from classes_network.Neuron import Neuron
import random


class Individual:
    def __init__(self, ID, receptors, call_create = True):
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
        if call_create:
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
        for i in list(self.neurons.keys()):
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
            if self.first_neurons[i].is_activated[0]:
                self.first_neurons[i].is_activated[0] = False
        for square in range(len(self.receptors)):
            if self.receptors[square].changed:
                self.receptors[square].changed = False
                self.first_neurons[str(square) + "_" + self.receptors[square].color].to[0].activate(self.first_neuron_depolarization)
                self.first_neurons[str(square) + "_" + self.receptors[square].color].is_activated[0] = True


    def depolarize_neurons(self):
        for i in self.neurons:
            self.neurons[i].depolarize()


    def manage_activated_neurons(self, body, effectors):
        for i in self.neurons:
            self.neurons[i].manage_activated(body, effectors)

    def depolarize_effectors(self):
        for i in self.effectors:
            self.effectors[i] = False

    def add_neuron(self, amount):
        list_of_ids = [int(i) for i in (list(self.neurons.keys()))]
        list_of_ids.sort()
        id_counter = list_of_ids[len(list_of_ids)-1]
        for i in range(amount):
            id_counter += 1
            self.neurons[str(id_counter)] = Neuron(str(id_counter), self.neurons[random.choice(list(self.neurons.keys()))])
            rec_neuron = random.choice(list(self.neurons.keys()))
            self.neurons[rec_neuron].to.append(self.neurons[str(id_counter)])
            self.neurons[rec_neuron].to_depolarization_rate.append(round(random.randint(0, 15), 2))
            self.neurons[rec_neuron].to_depolarization.append(round(random.random() * 2 - 1, 2))
            self.neurons[rec_neuron].current_dep_rate.append(0)
            self.neurons[rec_neuron].is_activated.append(False)

    def delete_neuron(self, amount):
        for i in range(amount):
            id = random.choice(list(self.neurons.keys()))
            del self.neurons[id]

    def clean_del_neurons(self):
        for i in self.neurons:
            for j in self.neurons[i].to:
                if not type(j) == str:
                    if j.ID not in list(self.neurons.keys()):
                        index = self.neurons[i].to.index(j)
                        self.neurons[i].to.remove(j)
                        self.neurons[i].current_dep_rate.pop(index)
                        self.neurons[i].to_depolarization_rate.pop(index)
                        self.neurons[i].to_depolarization.pop(index)
                        self.neurons[i].is_activated.pop(index)

        for i in self.first_neurons:
            for j in self.first_neurons[i].to:
                if j.ID not in list(self.neurons.keys()):
                    index = self.first_neurons[i].to.index(j)
                    self.first_neurons[i].to.remove(j)
                    self.first_neurons[i].current_dep_rate.pop(index)
                    self.first_neurons[i].to_depolarization_rate.pop(index)
                    self.first_neurons[i].to_depolarization.pop(index)
                    self.first_neurons[i].is_activated.pop(index)

    def add_synapses(self, amount):
        for i in range(amount):

            index = random.choice(list(self.neurons.keys()))
            self.neurons[index].to.append(self.neurons[random.choice(list(self.neurons.keys()))])
            self.neurons[index].to_depolarization_rate.append(round(random.randint(0, 15), 2))
            self.neurons[index].to_depolarization.append(round(random.random()*2-1, 2))
            self.neurons[index].current_dep_rate.append(0)
            self.neurons[index].is_activated.append(False)


    def delete_synapses(self, amount):
        for i in range(amount):
            index = random.choice(list(self.neurons.keys()))
            index_2 = random.choice(range(len(self.neurons[index].to) - 1)) if len(self.neurons[index].to) > 1 else 0
            if len(self.neurons[index].to) > 0:
                self.neurons[index].to.pop(index_2)
                self.neurons[index].to_depolarization_rate.pop(index_2)
                self.neurons[index].to_depolarization.pop(index_2)
                self.neurons[index].current_dep_rate.pop(index_2)
                self.neurons[index].is_activated.pop(index_2)
        for i in self.neurons:
            if len(self.neurons[i].to) == 0:
                del self.neurons[i]
                self.clean_del_neurons()


    def copy(self, other):
        for neuron in other.neurons:
            new_neuron = Neuron(other.neurons[neuron].ID, 0)
            self.neurons[other.neurons[neuron].ID] = new_neuron

        for neuron in other.neurons:

            new_neuron = self.neurons[neuron]

            new_neuron.repolarization = other.neurons[neuron].repolarization
            new_neuron.threshold = other.neurons[neuron].threshold


            new_neuron.to = []
            new_neuron.to_depolarization_rate = []
            new_neuron.to_depolarization = []
            new_neuron.current_dep_rate = []

            for i in range(len(other.neurons[neuron].to)):
                new_neuron.to_depolarization_rate.append(other.neurons[neuron].to_depolarization_rate[i])
                new_neuron.to_depolarization.append(other.neurons[neuron].to_depolarization[i])
                new_neuron.current_dep_rate.append(other.neurons[neuron].current_dep_rate[i])
                if type(other.neurons[neuron].to[i]) == str:
                    new_neuron.to.append(other.neurons[neuron].to[i])
                else:
                    new_neuron.to.append(self.neurons[other.neurons[neuron].to[i].ID])


        for first_neuron in other.first_neurons:
            new_neuron = Neuron(other.first_neurons[first_neuron].ID, 0)
            self.first_neurons[other.first_neurons[first_neuron].ID] = new_neuron

        for first_neuron in other.first_neurons:

            new_neuron = self.first_neurons[first_neuron]

            new_neuron.repolarization = other.first_neurons[first_neuron].repolarization
            new_neuron.threshold = other.first_neurons[first_neuron].threshold

            new_neuron.to = []
            new_neuron.to_depolarization_rate = []
            new_neuron.to_depolarization = []
            new_neuron.current_dep_rate = []

            for i in range(len(other.first_neurons[first_neuron].to)):
                new_neuron.to_depolarization_rate.append(other.first_neurons[first_neuron].to_depolarization_rate[i])
                new_neuron.to_depolarization.append(other.first_neurons[first_neuron].to_depolarization[i])
                new_neuron.current_dep_rate.append(other.first_neurons[first_neuron].current_dep_rate[i])

                if type(other.first_neurons[first_neuron].to[i]) == str:
                    new_neuron.to.append(other.first_neurons[first_neuron].to[i])
                else:
                    new_neuron.to.append(self.neurons[other.first_neurons[first_neuron].to[i].ID])


