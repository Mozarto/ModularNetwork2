from classes_network.Individual import Individual
import copy

EV_RATE_IND = 0.2
EV_RATE_NEU = 0.2

def add(lin):
    temp = lin.individuals.copy()
    filtered_ind_amount = int(EV_RATE_IND*lin.total_individuals)


    for i in temp:
        new_ind = []
        calc = int((lin.total_individuals-filtered_ind_amount)/filtered_ind_amount) if filtered_ind_amount != 0 else 0
        for j in range(calc):
            ind = Individual(str(lin.individuals_counter+1), i.receptors, False, i.ID)
            lin.individuals_counter += 1
            ind.copy(i)
            ind.delete_neuron(int((len(ind.neurons)*EV_RATE_NEU)/2))
            ind.delete_synapses(int((len(ind.neurons) * EV_RATE_NEU)))
            ind.add_neuron(int(len(ind.neurons) * EV_RATE_NEU))
            ind.add_synapses(int((len(ind.neurons)*EV_RATE_NEU)*2))
            ind.clean_del_neurons()
            new_ind.append(ind)
        lin.individuals += new_ind


def check(lin):
    for individual in lin.individuals:
        highest_to = 0
        tos = []
        tos2 = []
        len_to = 0
        lt = []
        for neuron in individual.neurons:
            if len(individual.neurons[neuron].current_dep_rate) > len_to:
                len_to = len(individual.neurons[neuron].current_dep_rate)
                lt = individual.neurons[neuron].current_dep_rate
            for to in individual.neurons[neuron].to:
                if not type(to) == str:
                    if int(to.ID) > highest_to:
                        highest_to = int(to.ID)
                    tos.append(to.ID)
                else:
                    tos2.append(to)

        print("ID: " + str(individual.ID))
        print("DT: " + str(individual.distance_travelled))
        print("LT: " + str(len_to))
        print(lt)
        print([i for i in list(individual.neurons.keys())])
        # print(tos)
        # print(tos2)
        print("HT: " + str(highest_to))
        print("----------------------------------------------------------------------------------")




def clean(lin):
    lin.individuals = lin.individuals[-int(len(lin.individuals)*EV_RATE_IND):]










