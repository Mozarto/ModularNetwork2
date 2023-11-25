from classes_network.Individual import Individual


class Lineage:
    def __init__(self, receptors, n_receptors, time, zoom, map_size):
        self.total_individuals = 2
        self.individuals = self.create_individuals(receptors)
        self.generations = 0

        self.n_receptors = n_receptors
        self.time = time
        self.zoom = zoom
        self.map_size = map_size

        self.remainder_ratio = 0.1
        self.successes = []
        self.failures = []

    def create_individuals(self, receptors):
        ind = []
        for i in range(self.total_individuals):
            ind.append(Individual(str(i+1), receptors))

        return ind
