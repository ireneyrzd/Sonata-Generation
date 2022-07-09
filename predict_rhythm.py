import pandas as pd
import numpy as np
import csv


class Predict:
    # constructor
    def __init__(self, transition_file_name): #key, time signature
        # initialize variables
        self.transition = []
        self.data = []
        self.states = []
        self.current_onset = 1
        self.last_note = ''
        self.first = False
        #num_of_onsets = num_of_measures * 4 #time signature
        self.rhythm = [] #output rhythm

        #copy csv data into list data
        with open(transition_file_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self.data.append(row)
        for i in range(1, len(self.data[0])):
            self.states.append(self.data[0][i])
            self.transition.append(self.data[i])
        self.transition = np.delete(self.transition, 0, 1).astype(float)


    def find_note(self, first):
        self.first = first
        current_state = np.random.random()
        cumulative = 0
        for i in range(len(self.states)):
            x = ''
            if self.first:
                x = self.last_note
            else:
                x = self.rhythm[-1]
            #print('state[i]', self.states[i], 'x', x, self.states[i] == x)
            if self.states[i] == x:
                for j in range(1, len(self.states)):
                    cumulative += self.transition[j][i]
                    #print('current', current_state, 'cumulative', cumulative, current_state < cumulative)
                    if current_state < cumulative:
                        return self.states[j]
        return 'Unable to generate rhythm'

    def predict(self, num_of_measures, start_note):
        for i in range(num_of_measures):
            #print (self.rhythm)
            current_onset = 1
            if i == 0:
                self.rhythm.append(start_note)
                current = ''
                if self.first:
                    current = self.last_note
                else:
                    current = self.rhythm[-1]
                index1 = 0
                for k in range(len(current)):
                    if current[k] == '_':
                        index1 = k+1
                        break
                current_onset += float(current[index1:-1])
            found = False
            while current_onset < 4.998 and not found: #reduce float point error
                self.rhythm.append(self.find_note(False))
                current = self.rhythm[-1]
                index1 = 0
                for k in range(len(current)):
                    if current[k] == '_':
                        index1 = k+1
                        found = True
                        break
                current_onset += float(current[index1:-1])
            #self.rhythm.append('|')
        #print('rhythm', self.rhythm)
        self.last_note = self.rhythm[-1]
        return self.rhythm


# rh = Predict("high_voice_transition.csv")
# rh_theme1 = rh.predict(4, '1.0N')
# print(rh_theme1) #sentence 1

# print('Right hand rhythm: ')
# rh = Predict("high_voice_transition.csv", 4, '1.0N')
# print(rh.predict())

# print('Left hand rhythm: ')
# lh = Predict("low_voice_transition.csv", 8, '2.0C')
# print(lh.predict())