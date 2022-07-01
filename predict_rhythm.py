import numpy as np
import pandas as pd
import csv



def predict_rhythm(transition_file_name):
    transition = []
    data = []
    states = []
    current_state = []
    #copy csv data into list data
    with open(transition_file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            data.append(row)
    for i in range(1, len(data[0])):
        states.append(data[0][i])
        transition.append(data[i])
        if states[i-1] == '2.0C':
            current_state.append(1.0)
        else:
            current_state.append(0.0)  
    transition = np.delete(transition, 0, 1).astype(float)
    # print(states)
    # print(initial_states)
    # print(transition)
    start = '1.0N'
    number_of_onsets = 12
    rhythm = [start]
    index = 0
    for i in range(number_of_onsets):
        current_state = np.matmul(current_state, transition)
        for j in range(len(states)-1):
            if current_state[j+1] > current_state[j]:
                index = j+1
        rhythm.append(states[j])
    return rhythm

print('Right hand rhythm: ')
print(predict_rhythm('high_voice_transition.csv'))

print('Left hand rhythm: ')
print(predict_rhythm('low_voice_transition.csv'))
