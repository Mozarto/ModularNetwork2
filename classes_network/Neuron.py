import random

class Neuron:
    def __init__(self, ID, to):
        self.ID = ID
        self.to = [to]
        #{"ID": [signal_speed, depolarization_magnitude]}
        self.threshold = round(((random.random()*10)-5), 2) # How much to activate neuron
        self.to_depolarization_rate = [round(random.randint(0, 15), 2)] #How many turns it will take to reach next neuron
        self.repolarization = round(random.randint(0, 100)/100, 2) #Ratio of how many turns it takes for the current potential to reach zero again
        self.to_depolarization = [round(random.random()*2-1, 2)] #How much it will influence next neuron

        self.current_threshold = 0

        self.is_activated = [False]
        self.current_dep_rate = [0]

    def activate(self, add_threshold):
        self.current_threshold += add_threshold
        # if len(self.to) > 1:
        #     print(len(self.to))
        #     print(self.current_dep_rate)
        #     print(self.to_depolarization_rate)
        #     print(self.to_depolarization)
        #     print("----------------------------------")
        if self.current_threshold > self.threshold:
            for i in range(len(self.is_activated)):
                self.is_activated[i] = True

    def depolarize(self):
        self.current_threshold*=self.repolarization

    def manage_activated(self, body, effectors):
        ran = range(len(self.to)) if len(self.to) > 1 else [0]
        # if type(self.to[0]) != str:
            # print("ID: " + str(self.to[0].ID))
            # print("to: " + str([i.ID for i in self.to[0].to if not type(i) == str]))
            # print("current: " + str(self.to[0].current_dep_rate))
            # print("---------------------------------------------")
        for i in ran:
            if self.is_activated[i]:
                # if type(self.to[0]) != str:
                #     print("ID: " + str(self.to[0].ID))
                #     print("to: " + str([i.ID for i in self.to[0].to if not type(i) == str]))
                #     print("current: " + str(self.to[0].current_dep_rate))
                #     print("---------------------------------------------")

                self.current_dep_rate[i] += 1
                if self.current_dep_rate[i] >= self.to_depolarization_rate[i]:
                    self.current_dep_rate[i] = 0
                    self.is_activated[i] = False
                    if not type(self.to[i]) == str:
                        self.to[i].activate(self.to_depolarization[i])
                    else:
                        if self.to[i] == "up":
                            effectors["up"] = True
                            body.up()
                        elif self.to[i] == "down":
                            effectors["down"] = True
                            body.down()
                        elif self.to[i] == "right":
                            effectors["right"] = True
                            body.right()
                        elif self.to[i] == "left":
                            effectors["left"] = True
                            body.left()



