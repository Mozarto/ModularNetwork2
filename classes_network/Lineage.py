from classes_network.Individual import Individual


class Lineage:
    def __init__(self, receptors, n_receptors, time, zoom, map_size, create_individuals = True):
        self.database_id = -1,
        self.generation = 0
        self.total_individuals = 10
        self.individuals_counter = 0
        self.individuals = []
        if create_individuals:
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
            self.individuals_counter += 1

        return ind

    def bubble_sort(self):
        n = len(self.individuals)

        for i in range(n):

            already_sorted = True

            for j in range(n - i - 1):
                if self.individuals[j].score > self.individuals[j + 1].score:

                    self.individuals[j], self.individuals[j + 1] = self.individuals[j + 1], self.individuals[j]

                    already_sorted = False

            if already_sorted:
                break

        for i in range(n):

            already_sorted = True

            for j in range(n - i - 1):
                if self.individuals[j].distance_travelled > self.individuals[j + 1].distance_travelled:

                    self.individuals[j], self.individuals[j + 1] = self.individuals[j + 1], self.individuals[j]

                    already_sorted = False

            if already_sorted:
                break


