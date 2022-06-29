import numpy as np
import pandas as pd
import csv

#TO DO : if one voice, use middle note decided a previous onsets of the measure to decide voice to accomdate
# right hand scales that go below central C (eg. measure 79), same thing for left hand. need to create array 
# to store previous onsets
# use tuples as representation object structured of chords (length, chord[boolean])
# consider putting high and low voice in seperate or same matrix

#copy csv data into list data
data = []
with open('20-notes.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
    for row in csv_reader:
        data.append(row)

#print(data)

#return true if two notes are in an interval/chord
def is_chord(a1, a2, b1, b2):
    if not(a1 == b1 and a2 == b2):
        return False
    return True

#split data into high (RH) and low (LH) voice
high_voice = []
low_voice = []
for i in range(len(data)):
    if data[i][-2] == 1:
        low_voice.append(data[i])
    else: 
        high_voice.append(data[i])

def append_rest(arr, data, rest_duration):
    arr.append([str(data[0] + data[3]), '0.0', '0.0', str(rest_duration), str(data[4]), str(data[5]), 'R'])
      
#adds rests into data
#label duration R for rest
#label duration C for chords/interval
#label duration N for notes
def adds_rests(dataset, file_name):
    data = []
    i = 0
    while i < len(dataset)-1:
        #print(i)
        if is_chord(dataset[i][0], dataset[i][3], dataset[i+1][0], dataset[i+1][3]):
            #print('c')
            data.append(np.append(dataset[i], 'C'))
        elif is_chord(dataset[i-1][0], dataset[i-1][3], dataset[i][0], dataset[i][3]):
            #print('c')
            data.append(np.append(dataset[i], 'C'))
        else:
            #print('n')
            data.append(np.append(dataset[i], 'N'))
        rest_dur = dataset[i+1][0] - dataset[i][0] - dataset[i][3]
        if (dataset[i+1][0] - dataset[i][0] > 0.0001 and rest_dur > 0.0001):
            append_rest(data, dataset[i], rest_dur)
                                      
        i+=1
    with open(file_name, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(data)
    return data


high_voice = adds_rests(high_voice, 'higher_voice.csv')
low_voice = adds_rests(low_voice, 'lower_voice.csv')


# print('high: ')
# print(high_voice)
# print()
# print('low: ')
# print(low_voice)


#create transition vectors
def create_transition(data_list, file_name):
    #remove instances of stacked notes in data with equal length 
    # !! needs better chord analysis
    data_short = []
    for i in range(len(data_list)-1):
        if is_chord(data[i][0], data[i][3], data[i+1][0], data[i+1][3]):
            data_short.append(data_list[i])
    #print(data_short)
    states = [] #sorted array with all possible note values
    note_val = [] #column 4 of data, sequenced note value
    for i in range(len(data_short)):
        note_val.append(data_short[i][3] + data_short[i][6])
        if data_short[i][3] + data_short[i][6] not in states:
            states.append(data_short[i][3] + data_short[i][6])
    states.sort()
    #print(states)
    transition = pd.crosstab(pd.Series(note_val[1:],name='succeeding note value'),
                             pd.Series(note_val[:-1],name='current note value'),normalize=1)

    df = pd.DataFrame(transition)
    df.to_csv(file_name)
    return transition


print('high voice: ')
print(create_transition(high_voice, 'high_voice_transition.csv'))
print()
print('low voice: ')
print(create_transition(low_voice, 'low_voice_transition.csv'))
