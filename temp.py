import numpy as np
import pandas as pd
import csv

def most_frequent(List):
        counter = 0
        num = List[0]
        
        for i in List:
            curr_frequency = List.count(i)
            if(curr_frequency> counter):
                counter = curr_frequency
                num = i

        return num 

def csv_to_arr(file_name):
    #copy csv data into list data
    chord_data = []
    with open('20-chords.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            chord_data.append(row)

    # struc_data = []
    # with open('20-phrases.csv') as csv_file:
    #     csv_reader = csv.reader(csv_file, delimiter=',')
    #     for row in csv_reader:
    #         struc_data.append(row)

    chord_data_long = []
    chord_data_long.append(np.concatenate(([0], chord_data[0][2:7])).tolist())
    i = 1
    for j in range (len(chord_data)):
        while i < float(chord_data[j][1]):
            chord_data_long.append(np.concatenate(([i], chord_data[j][2:7])).tolist())
            i+=1
    #print(chord_data_long)

    chord_data_short = []
    for i in range(0, len(chord_data_long), 4):
        temp = []
        for j in range(i, i+4):
            #print(j)
            temp = np.append(temp, chord_data_long[j][-1]).tolist()
        chord_data_short = np.append(chord_data_short, most_frequent(temp))
    return chord_data_short

csv_to_arr('20-chords.csv')

def block(weight, lead, follow): #rules, length?
    block = {
        'weight': weight,
        'lead': lead,
        'follow': follow,
        #'rules': rules,
        #'length': length,
    }
    return block

def create_weight():
    arr = []
    rules = csv_to_arr('20-notes.csv')
    for i in range (len(rules) - 1):
        found = False
        for j in range(len(arr)):
            if arr[j]["lead"] == rules[i] and arr[j]["follow"] == rules[i+1]:
                arr[j]['weight'] += 1
                found = True
                break
        if not found:
            arr.append(block(1, rules[i], rules[i+1]))
    return arr

print(create_weight())

