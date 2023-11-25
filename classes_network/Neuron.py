import random

class Neuron:
    def __init__(self, ID, to):
        self.ID = ID
        self.to = to
        #{"ID": [signal_speed, depolarization_magnitude]}
        self.threshold = (random.random()*10)-5 # How much to activate neuron
        self.to_depolarization_rate = random.randint(0, 15) #How many turns it will take to reach next neuron
        self.repolarization = random.randint(0, 100)/100 #Ratio of how many turns it takes for the current potential to reach zero again
        self.to_depolarization = random.random()*2-1 #How much it will influence next neuron

        self.current_threshold = 0

        self.is_activated = False
        self.current_dep_rate = 0

    def activate(self, add_threshold, effectors = None, body = None):
        self.current_threshold += add_threshold
        if self.current_threshold > self.threshold:
            #print("called activated")
            #print("1. " + str(self.current_threshold) + " 2. " + str(self.threshold))
            self.is_activated = True

    def depolarize(self):
        self.current_threshold*=self.repolarization
        #print("1. "+str(self.current_threshold)+" 2. "+str(self.threshold))

    def manage_activated(self, body, effectors):
        #print("is: "+str(self.is_activated))
        if self.is_activated:
            self.current_dep_rate += 1
            #print("is_activated: "+str(self.to_depolarization_rate)+" / "+str(str(self.current_dep_rate)))
            #print("2. " + str(self.current_dep_rate) + " 3. " + str(self.to_depolarization_rate))
            if self.current_dep_rate >= self.to_depolarization_rate:
                self.current_dep_rate = 0
                self.is_activated = False
                if not type(self.to) == str:
                    self.to.activate(self.to_depolarization, body, effectors)
                    # print("what hell" + str(self.is_activated))
                else:
                    # print("reaches the end")
                    # print(self.to)
                    if self.to == "up":
                        effectors["up"] = True
                        body.up()
                    elif self.to == "down":
                        effectors["down"] = True
                        body.down()
                    elif self.to == "right":
                        effectors["right"] = True
                        body.right()
                    elif self.to == "left":
                        effectors["left"] = True
                        body.left()



