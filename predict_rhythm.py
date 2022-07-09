import pandas as pd
import numpy as np
import csv


class Predict:
    # constructor
    def __init__(self, transition_file_name, num_of_measures, start_note): #key, time signature
        # initialize variables
        self.transition = []
        self.data = []
        self.states = []
        self.num_of_measures = num_of_measures
        self.current_onset = 1
        #num_of_onsets = num_of_measures * 4 #time signature
        self.start_note = '1.0_' + start_note #starting note
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


    def find_note(self):
        current_state = np.random.random()
        cumulative = 0
        for i in range(len(self.states)):
            if self.states[i] == self.rhythm[-1]:
                for j in range(1, len(self.states)):
                    cumulative += self.transition[j][i]
                    if current_state < cumulative:
                        return self.states[j]
        return 'Unable to generate rhythm'        

    def predict(self):
        for i in range(self.num_of_measures):
            #print (self.rhythm)
            current_onset = 1
            if i == 0:
                self.rhythm.append(self.start_note)
                current = self.rhythm[-1]
                index1 = 0
                for k in range(len(current)):
                    if current[k] == '_':
                        index1 = k+1
                        break
                current_onset += float(current[index1:-1])
            while current_onset < 4.98: #reduce float point error
                self.rhythm.append(self.find_note())
                current = self.rhythm[-1]
                index1 = 0
                for k in range(len(current)):
                    if current[k] == '_':
                        index1 = k+1
                        break
                current_onset += float(current[index1:-1])
            #self.rhythm.append('|')
        return self.rhythm


print('Right hand rhythm: ')
rh = Predict("high_voice_transition.csv", 4, '1.0N')
print(rh.predict())

print('Left hand rhythm: ')
lh = Predict("low_voice_transition.csv", 8, '2.0C')
print(lh.predict())