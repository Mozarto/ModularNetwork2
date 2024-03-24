from tkinter import *
from functools import partial
import time

from Database_classes.Get import database_get, do_query, delete_from_db
from classes_network.Evolution import EV_RATE_IND
from sim_start import sim
from classes_network.Lineage import Lineage
from classes_network.Individual import Individual
from classes_network.Neuron import Neuron
from classes_sim.View import View
from classes_neuron_sim.ManageNeurons import ManageNeurons
from Database_classes.Save import *
from classes_network import Evolution




def main():
    def load_lin():
        def _on_mousewheel(event):
            listbox.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _bound_to_mousewheel(event, mousewheel_frame):
            try:
                mousewheel_frame.canvas.unbind_all("<MouseWheel>")
            except AttributeError:
                pass
            listbox.bind("<MouseWheel>", _on_mousewheel)

        def _unbound_to_mousewheel(event, mousewheel_frame):
            listbox.unbind("<MouseWheel>")
            try:
                mousewheel_frame.canvas.bind_all("<MouseWheel>",
                                                      lambda e: mousewheel_frame.canvas.yview_scroll(
                                                          int(-1 * (e.delta / 120)), "units"))
            except AttributeError:
                pass

        frame = Frame(root)
        frame.grid(row=0, column=0, sticky=NSEW)

        frame.rowconfigure(index=0, weight=1)
        frame.rowconfigure(index=1, weight=1)
        frame.rowconfigure(index=2, weight=1)
        #frame.rowconfigure(index=3, weight=1)

        frame.columnconfigure(index=0, weight=1)
        frame.columnconfigure(index=1, weight=1)
        frame.columnconfigure(index=2, weight=1)
        frame.columnconfigure(index=3, weight=1)


        scroll_list_frame = Frame(frame)
        scroll_list_frame.grid(row=1, column=1, sticky=NSEW, columnspan=2)
        scroll_list_frame.columnconfigure(0, weight=99)
        scroll_list_frame.columnconfigure(1, weight=1)
        scroll_list_frame.rowconfigure(0, weight=1)

        listbox = Listbox(master=scroll_list_frame)
        listbox.grid(row=0, column=0, sticky=NSEW)

        scrollbar = Scrollbar(scroll_list_frame, orient="vertical", command=listbox.yview)
        listbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky=NSEW)

        values = database_get("lineages", ["id", "name"], "Database_classes/modular_network.db")

        for i in range(len(values)):
            listbox.insert(values[i][0], str(values[i][0]) + "    " + values[i][1])

        accept_btn = Button(

            text="Start", master=frame, padx=30, command=partial(set_sim_load, listbox)
        )
        decline_button = Button(
            text="Back", master=frame, command=lambda: main_frame.tkraise(), padx=30
        )

        accept_btn.grid(row=2, column=1)
        decline_button.grid(row=2, column=2)

        frame.tkraise()

        listbox.bind('<Enter>', partial(_bound_to_mousewheel, scroll_list_frame))
        listbox.bind('<Leave>', partial(_unbound_to_mousewheel, scroll_list_frame))



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
        frame.rowconfigure(index=8, weight=1)
        frame.rowconfigure(index=9, weight=2)

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
        entry_time.insert(0, "300")
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

        answers = [
            entry_time,
            entry_size,
            entry_zoom,
            entry_food,
            entry_tree,
            entry_name,
        ]

        var1 = IntVar()

        accept_btn = Button(
            text="Start", master=frame, command=partial(prep_answers, root, answers), padx=30
        )
        decline_button = Button(
            text="Back", master=frame, command=lambda: main_frame.tkraise(), padx=30
        )

        accept_btn.grid(row=7, column=1)
        decline_button.grid(row=7, column=2)

        frame.tkraise()

    # Main menu window initialization
    root = Tk()
    root.title("Sim Window") # "Main Menu Window"
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    screen_width = root.winfo_screenwidth()     #
    screen_height = root.winfo_screenheight()   #
    root_width = 600
    root_height = 400
    root.geometry(                              #
        f"{int(root_width)}x{int(root_height)}+{int(screen_width / 2 - root_width / 2)}+{int(screen_height / 2 - root_height / 2)}"
    )

    main_frame = Frame(root)

    main_frame.grid(row=0, column=0, sticky=NSEW)

    main_frame.rowconfigure(index=0, weight=4)
    main_frame.rowconfigure(index=1, weight=1)
    main_frame.rowconfigure(index=2, weight=1)
    main_frame.rowconfigure(index=3, weight=4)

    main_frame.columnconfigure(0, weight=1)

    btn_new = Button(
        text="New lineage", master=main_frame, command=new_lin, pady=10, padx=30
    )
    btn_new.grid(row=1, column=0)

    btn_load = Button(
        text="Load lineage", master=main_frame, command=load_lin, pady=10, padx=30
    )
    btn_load.grid(row=2, column=0)

    root.mainloop()

def set_sim_load(listbox):
    id = listbox.get(first=listbox.curselection()).split("    ")[0] if not listbox.curselection() == () else -1
    if id == -1:
        return

    values = database_get("lineages WHERE id="+str(id), ["*"], "Database_classes/modular_network.db")
    values = values[0]

    # Simulation screen variables
    screen_width = 1200
    screen_height = 675
    screen_size = (screen_width, screen_height)
    screen_border = 5

    # Surface screen variables
    screen_size_surfaces = (
        screen_size[0] / 4 - screen_border * 2,
        screen_size[1] / 4 - screen_border * 2,
    )

    square_size = 10
    view = View(screen_size_surfaces, square_size)

    lin = Lineage(
        view.squares,
        square_size,
        int(values[6]),
        int(values[5]),
        int(values[7]),
        False
    )

    last_gen = do_query("SELECT * FROM lineages WHERE id="+str(id), "Database_classes/modular_network.db")
    print(last_gen)

    gen = do_query("SELECT MAX(generation) FROM individuals WHERE lineage="+str(id), "Database_classes/modular_network.db")[0][0]
    n_ind = database_get("individuals WHERE lineage="+str(id)+" AND generation = "+str(gen), ["*"], "Database_classes/modular_network.db")


    if len(n_ind) < int(lin.total_individuals*EV_RATE_IND):
        delete_from_db("individuals", "generation = "+str(last_gen), "Database_classes/modular_network.db")
        return

    for ind in n_ind:
        individual = Individual(ind[0], view.squares, False)
        n_neuron = database_get("neurons WHERE individual=" + str(ind[0]) + " AND first_neuron = 0", ["*"], "Database_classes/modular_network.db")

        if len(n_neuron) == 0:
            delete_from_db("individuals", "generation = " + str(last_gen), "Database_classes/modular_network.db")
            return

        for n in n_neuron:
            new_neuron = Neuron(n[1], [])
            individual.neurons[n[1]] = new_neuron
        for n in n_neuron:
            to = []

            for o in n[4].split("*"):
                i = o.strip()
                if i not in list(individual.effectors.keys()):
                    to.append(individual.neurons[i])
                else:
                    to.append(i)
            dep_rate = []
            for o in n[6].split("*"):
                i = o.strip()
                dep_rate.append(int(i))
            dep = []
            for o in n[8].split("*"):
                i = o.strip()
                dep.append(float(i))

            individual.neurons[n[1]].to = to
            individual.neurons[n[1]].to_depolarization_rate = dep_rate
            individual.neurons[n[1]].to_depolarization = dep

            individual.neurons[n[1]].adjust_lists()

        n_first_neuron = database_get("neurons WHERE individual=" + str(ind[0]) + " AND first_neuron = 1", ["*"],
                                "Database_classes/modular_network.db")
        for n in n_first_neuron:
            new_neuron = Neuron(n[1], [])
            individual.first_neurons[n[1]] = new_neuron

        for n in n_first_neuron:
            to = []
            for o in n[4].split("*"):
                i = o.strip()
                to.append(individual.neurons[i])
            dep_rate = []
            for o in n[6].split("*"):
                i = o.strip()
                dep_rate.append(int(i))
            dep = []
            for o in n[8].split("*"):
                i = o.strip()
                dep.append(float(i))

            individual.first_neurons[n[1]].to = to


            individual.first_neurons[n[1]].to_depolarization_rate = dep_rate
            individual.first_neurons[n[1]].to_depolarization = dep

            individual.first_neurons[n[1]].adjust_lists()

        #(28241, '303_blue', 11, 1, '299 ', -3.34, '5', 0.76, '-0.34')
        lin.individuals.append(individual)

    gen = last_gen

    run = True

    while run:

        gen += 1
        counter = 0
        for ind in lin.individuals:
            counter += 1
            manage_neurons = ManageNeurons(
                ind.first_neurons, ind.neurons, ind.effectors
            )

            ind_score = sim(
                screen_size=screen_size,
                screen_border=screen_border,
                screen_size_surfaces=screen_size_surfaces,
                ind=ind,
                view=view,
                time=int(values[5]),
                neuron_manager=manage_neurons,
                zoom=int(values[4]),
                map_size=int(values[6]),
                food_timer=int(values[7]),
                food_density=int(values[8]),
                gen=gen,
                ind_counter=counter
            )


            ind.score = ind_score[0]
            ind.distance_travelled = ind_score[1]
            run = ind_score[2]
            if not ind_score[2]:
                break

        lin.bubble_sort()
        if run:
            # Evolution.check(lin)
            Evolution.clean(lin)
            # save(answers, lin, gen)
            Evolution.add(lin)

def prep_answers(root, answers):
    answers = [
        answers[0].get(),
        answers[1].get(),
        answers[2].get(),
        answers[3].get(),
        answers[4].get(),
        answers[5].get(),
    ]
    set_sim_new(root, answers)


def set_sim_new(root, answers):
    # screen_width = root.winfo_screenwidth()
    # screen_height = root.winfo_screenheight()

    screen_width = 1200
    screen_height = 675

    screen_size = (screen_width, screen_height)
    screen_border = 5

    screen_size_surfaces = (
        screen_size[0] / 4 - screen_border * 2,
        screen_size[1] / 4 - screen_border * 2,
    )

    square_size = 10
    view = View(screen_size_surfaces, square_size)

    lin = Lineage(
        view.squares,
        square_size,
        int(answers[0]),
        int(answers[2]),
        int(answers[1]),
    )

    new_lin(answers, lin)

    gen = 0

    run = True

    while run:

        gen += 1
        counter = 0
        for ind in lin.individuals:
            counter += 1
            manage_neurons = ManageNeurons(
                ind.first_neurons, ind.neurons, ind.effectors
            )

            ind_score = sim(
                screen_size=screen_size,
                screen_border=screen_border,
                screen_size_surfaces=screen_size_surfaces,
                ind=ind,
                view=view,
                time=int(answers[0]),
                neuron_manager=manage_neurons,
                zoom=int(answers[2]),
                map_size=int(answers[1]),
                food_timer=int(answers[3]),
                food_density=int(answers[4]),
                gen=gen,
                ind_counter=counter
            )

            ind.score = ind_score[0]
            ind.distance_travelled = ind_score[1]
            run = ind_score[2]
            gen_querry = "UPDATE lineages SET generation = "+ str(gen+1) +" where id = " + str(lin.database_id)

            do_query(gen_querry, "Database_classes/modular_network.db")



            if not ind_score[2]:
                break

        lin.bubble_sort()
        if run:
            #Evolution.check(lin)
            Evolution.clean(lin)
            save(lin, gen)
            Evolution.add(lin)



def new_lin(answers, lin):
    values = {
        "name": answers[5],
        "n_individuals": len(lin.individuals),
        "n_receptors": lin.n_receptors,
        "zoom": int(answers[2]),
        "gen_time": int(answers[0]),
        "map_size": int(answers[1]),
        "food_timer": int(answers[3]),
        "food_density": int(answers[4]),
        "generation": 0
    }

    insert_lineage(values, "Database_classes/modular_network.db")

    lin.database_id = int(database_get(
            "lineages ORDER BY id DESC LIMIT 1",
            ["id"],
            "Database_classes/modular_network.db",
        )[0][0])

def save(lin, gen):
    for ind in lin.individuals:
        values = {
            "id_lin":ind.ID,
            "origin":ind.origin,
            "lineage": lin.database_id,
            "score": ind.score,
            "distance_travelled": ind.distance_travelled,
            "generation":gen
        }

        insert_individuals(values, "Database_classes/modular_network.db")

        ind_id = int(database_get(
            "individuals ORDER BY id DESC LIMIT 1",
            ["id"],
            "Database_classes/modular_network.db",
        )[0][0])

        for n in ind.first_neurons:

            to_string = ""
            for to in ind.first_neurons[n].to:
                to_string += to.ID + "*"

            to_string = to_string[:-1]


            to_dep_string = ""
            for to in ind.first_neurons[n].to_depolarization:
                to_dep_string += str(to) + "*"
            to_dep_string = to_dep_string[:-1]


            to_rate_string = ""

            for to in ind.first_neurons[n].to_depolarization_rate:
                to_rate_string += str(to) + "*"
            to_rate_string = to_rate_string[:-1]



            values = {
                "id_ind": ind.first_neurons[n].ID,
                "individual": ind_id,
                "first_neuron": 1,
                "to_neuron": to_string,
                "threshold": ind.first_neurons[n].threshold,
                "to_depolarization_rate": to_rate_string,
                "repolarization": ind.first_neurons[n].repolarization,
                "to_depolarization": to_dep_string,
            }

            insert_neuron(values, "Database_classes/modular_network.db")

        for n in ind.neurons:

            to_string = ""
            for to in ind.neurons[n].to:
                if type(to) != str:
                    to_string += to.ID + "*"
                else:
                    to_string += to + "*"

            to_string = to_string[:-1]


            to_dep_string = ""
            for to in ind.neurons[n].to_depolarization:
                to_dep_string += str(to) + "*"
            to_dep_string = to_dep_string[:-1]

            to_rate_string = ""
            for to in ind.neurons[n].to_depolarization_rate:
                to_rate_string += str(to) + "*"
            to_rate_string = to_rate_string[:-1]


            if type(ind.neurons[n].to) == str:
                values = {
                    "id_ind": ind.neurons[n].ID,
                    "individual": ind_id,
                    "first_neuron": 0,
                    "to_neuron": to_string,
                    "threshold": ind.neurons[n].threshold,
                    "to_depolarization_rate": to_rate_string,
                    "repolarization": ind.neurons[n].repolarization,
                    "to_depolarization": to_dep_string,
                }
            else:
                values = {
                    "id_ind": ind.neurons[n].ID,
                    "individual": ind_id,
                    "first_neuron": 0,
                    "to_neuron": to_string,
                    "threshold": ind.neurons[n].threshold,
                    "to_depolarization_rate": to_rate_string,
                    "repolarization": ind.neurons[n].repolarization,
                    "to_depolarization": to_dep_string,
                }

            insert_neuron(values, "Database_classes/modular_network.db")

main()
