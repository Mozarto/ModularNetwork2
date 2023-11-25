from tkinter import *
from functools import partial

from Database_classes.Get import database_get
from sim_start import sim
from classes_network.Lineage import Lineage
from classes_sim.View import View
from classes_neuron_sim.ManageNeurons import ManageNeurons
from Database_classes.Save import *


def main():
    def new_lin():
        frame = Frame(root)
        frame.grid(row=0, column=0, sticky=NSEW)

        frame.rowconfigure(index=0, weight=2)
        frame.rowconfigure(index=1, weight=1)
        frame.rowconfigure(index=2, weight=1)
        frame.rowconfigure(index=3, weight=1)
        frame.rowconfigure(index=4, weight=1)
        frame.rowconfigure(index=5, weight=1)
        frame.rowconfigure(index=6, weight=1)
        frame.rowconfigure(index=7, weight=1)
        frame.rowconfigure(index=8, weight=2)

        frame.columnconfigure(0, weight=4)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        frame.columnconfigure(3, weight=4)

        # -----------------------------------

        label_name = Label(frame, text="Name of lineage: ")
        label_name.grid(row=1, column=1, sticky=W)

        entry_name = Entry(frame)
        entry_name.insert(0, "New_Lineage")
        entry_name.grid(row=1, column=2)

        # -----------------------------------

        label_time = Label(frame, text="Cicles per simulation: ")
        label_time.grid(row=2, column=1, sticky=W)

        entry_time = Entry(frame)
        entry_time.insert(0, "450")
        entry_time.grid(row=2, column=2)

        # -----------------------------------

        label_size = Label(frame, text="Size of the map: ")
        label_size.grid(row=3, column=1, sticky=W)

        entry_size = Entry(frame)
        entry_size.insert(0, "5")
        entry_size.grid(row=3, column=2)

        # -----------------------------------

        label_zoom = Label(frame, text="Zoom: ")
        label_zoom.grid(row=4, column=1, sticky=W)

        entry_zoom = Entry(frame)
        entry_zoom.insert(0, "2")
        entry_zoom.grid(row=4, column=2)

        # -----------------------------------

        label_food = Label(frame, text="Cicles for food to appear: ")
        label_food.grid(row=5, column=1, sticky=W)

        entry_food = Entry(frame)
        entry_food.insert(0, "600")
        entry_food.grid(row=5, column=2)

        # -----------------------------------

        label_tree = Label(frame, text="Density of trees: ")
        label_tree.grid(row=6, column=1, sticky=W)

        entry_tree = Entry(frame)
        entry_tree.insert(0, "10000")
        entry_tree.grid(row=6, column=2)

        # -----------------------------------

        answers = [entry_time, entry_size, entry_zoom, entry_food, entry_tree, entry_name]

        accept_btn = Button(text="Start", master=frame, command=partial(set_sim, root, answers), padx=30)
        decline_button = Button(text="Back", master=frame, command=lambda: main_frame.tkraise(), padx=30)

        accept_btn.grid(row=7, column=1)
        decline_button.grid(row=7, column=2)

        frame.tkraise()

    root = Tk()

    root.title('Sim Window')

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root_width = 600
    root_height = 400
    root.geometry(
        f"{int(root_width)}x{int(root_height)}+{int(screen_width / 2 - root_width / 2)}+{int(screen_height / 2 - root_height / 2)}")

    main_frame = Frame(root)

    main_frame.grid(row=0, column=0, sticky=NSEW)

    main_frame.rowconfigure(index=0, weight=4)
    main_frame.rowconfigure(index=1, weight=1)
    main_frame.rowconfigure(index=2, weight=1)
    main_frame.rowconfigure(index=3, weight=4)

    main_frame.columnconfigure(0, weight=1)

    btn_new = Button(text="New lineage", master=main_frame, command=new_lin, pady=10, padx=30)
    btn_new.grid(row=1, column=0)

    btn_load = Button(text="Load lineage", master=main_frame, command=new_lin, pady=10,
                      padx=30)  # partial(set_sim, root)
    btn_load.grid(row=2, column=0)

    root.mainloop()


def set_sim(root, answers):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    screen_size = (screen_width, screen_height)
    screen_border = 5

    screen_size_surfaces = (screen_size[0] / 4 - screen_border * 2, screen_size[1] / 4 - screen_border * 2)

    square_size = 10
    view = View(screen_size_surfaces, square_size)

    lin = Lineage(view.squares, square_size, int(answers[0].get()), int(answers[2].get()), int(answers[1].get()))

    gen = 0

    for ind in lin.individuals:

        manage_neurons = ManageNeurons(ind.first_neurons, ind.neurons, ind.effectors)

        ind_score = sim(screen_size=screen_size, screen_border=screen_border,
                        screen_size_surfaces=screen_size_surfaces, ind=ind, view=view, time=int(answers[0].get()),
                        neuron_manager=manage_neurons,
                        zoom=int(answers[2].get()), map_size=int(answers[1].get()), food_timer=int(answers[3].get()), food_density=int(answers[4].get()))

        ind.score = ind_score[0]
        ind.distance_travelled = ind_score[1]


    values = {
        "name": answers[5].get(),
        "n_individuals": len(lin.individuals),
        "generations": gen,
        "n_receptors": len(view.squares),
        "zoom": int(answers[2].get()),
        "gen_time": int(answers[0].get()),
        "map_size": int(answers[1].get()),
        "food_timer": int(answers[3].get()),
        "food_density": int(answers[4].get())
    }

    insert_lineage(values, "Database_classes/modular_network.db")

    for ind in lin.individuals:
        values = {"lineage":int(database_get("lineages ORDER BY id DESC LIMIT 1", ["id"], "Database_classes/modular_network.db")[0][0]),
                             "score":ind.score, "distance_travelled":ind.distance_travelled}
        insert_individuals(values, "Database_classes/modular_network.db")
        for n in ind.first_neurons:
            values = {"id_ind":ind.first_neurons[n].ID,
                      "individual":int(database_get("lineages ORDER BY id DESC LIMIT 1", ["id"], "Database_classes/modular_network.db")[0][0]),
                      "first_neuron":1, "to_neuron":ind.first_neurons[n].to.ID,
                      "threshold":ind.first_neurons[n].threshold,
                      "to_depolarization_rate":ind.first_neurons[n].to_depolarization_rate,
                      "repolarization":ind.first_neurons[n].repolarization,
                      "to_depolarization":ind.first_neurons[n].to_depolarization}
            insert_neuron(values, "Database_classes/modular_network.db")
        for n in ind.neurons:
            if type(ind.neurons[n].to) == str:
                values = {"id_ind": ind.neurons[n].ID, "individual": int(
                    database_get("lineages ORDER BY id DESC LIMIT 1", ["id"], "Database_classes/modular_network.db")[0][0]),
                        "first_neuron": 0, "to_neuron": ind.neurons[n].to,
                        "threshold": ind.neurons[n].threshold,
                        "to_depolarization_rate": ind.neurons[n].to_depolarization_rate,
                        "repolarization": ind.neurons[n].repolarization,
                        "to_depolarization": ind.neurons[n].to_depolarization}
            else:
                values = {"id_ind": ind.neurons[n].ID, "individual": int(
                    database_get("lineages ORDER BY id DESC LIMIT 1", ["id"], "Database_classes/modular_network.db")[0][
                        0]),
                          "first_neuron": 0, "to_neuron": ind.neurons[n].to.ID,
                          "threshold": ind.neurons[n].threshold,
                          "to_depolarization_rate": ind.neurons[n].to_depolarization_rate,
                          "repolarization": ind.neurons[n].repolarization,
                          "to_depolarization": ind.neurons[n].to_depolarization}
            insert_neuron(values, "Database_classes/modular_network.db")


    print(database_get("neurons", ["*"], "Database_classes/modular_network.db"))


main()
