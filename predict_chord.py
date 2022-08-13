
import numpy as np
import pandas as pd
import csv
from random import randint


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
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            chord_data.append(row)

    # struc_data = []
    # with open('20-phrases.csv') as csv_file:
    #     csv_reader = csv.reader(csv_file, delimiter=',')
    #     for row in csv_reader:
    #         struc_data.append(row)


    # chord_data_long = []
    # for j in range (len(chord_data)):
    #     chord_data_long.append(chord_data[j][-1])
    # print (chord_data_long)
    chord_data_long = []
    chord_data_long.append(np.concatenate(([0], chord_data[0][2:7])).tolist())
    i = 1
    for j in range (len(chord_data)):
        while i < float(chord_data[j][1]):
            chord_data_long.append(np.concatenate(([i], chord_data[j][2:7])).tolist())
            i+=1
    # #print(chord_data_long)

    chord_data_short = []
    for i in range(0, len(chord_data_long) - 4, 4):
        temp = []
        for j in range(i, i+4):
            temp = np.append(temp, chord_data_long[j][-1]).tolist()
        chord_data_short = np.append(chord_data_short, most_frequent(temp))
    # print(chord_data_short)
    return chord_data_short

# csv_to_arr('20-chords.csv')

def rule(weight, lead, follow): #rules, length?
    rule = {
        'weight': weight,
        'lead': lead,
        'follow': follow,
        #'rules': rules,
        #'length': length,
    }
    return rule

# know what chord in what position
# for chord, store note/symbol/distance from root
def create_weight():
    arr = []
    data = []
    for i in [3, 9, 10, 20]:
        data = np.concatenate((data, csv_to_arr('dataset/' + str(i) + '/chords.csv')))
    for i in range (len(data) - 1):
        found = False
        for j in range(len(arr)):
            
            if arr[j]["lead"] == data[i] and arr[j]["follow"] == data[i+1]:
                arr[j]['weight'] += 1
                found = True
                break
        if not found:
            arr.append(rule(1, data[i], data[i+1]))
    # print(data)
    return arr

#print(create_weight())


# Matthew's code
def predict_chord(n):
    arr = create_weight()
    #print(create_weight())
    #END OF PREDICT_CHORD
    num_of_measures = n - 1
    chordPro = ['I']
    def find_follow(chords):
        sum = 0
        current_weight = 0
        #sum of weights
        for i in chords:
            sum += i['weight']
        #print(sum)
        n = randint(0, sum)
        #print(n)
        for i in range(len(chords)):
            current_weight += chords[i]['weight']
            if n <= current_weight:
                follow = chords[i]['follow']
                return follow
                break
    for i in range(num_of_measures):
        counter = 0
        dict_short = []
        #creates array based off lead chord
        for x in range(len(arr)):
            if chordPro[counter] == arr[x]['lead']:
                dict_short.append(arr[x])
        #print(dict_short)
        chordPro.append(find_follow(dict_short))
        counter += 1

    return chordPro

# chord_prog = predict_chord(16)
# print (chord_prog)