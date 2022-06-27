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

#split data into high (RH) and low (LH) voice
high_voice = []
low_voice = []
notes_in_onset = []
mid_notes_in_measure = []
row_num = 0
for onset in range(0, int(data[-1][0]) + 1):
    row_num_old = row_num
    while row_num < len(data) and data[row_num][0] <= onset:
        notes_in_onset.append(data[row_num][1])
        row_num += 1  
    notes_in_onset.sort()
    #print(notes_in_onset)
    mid_note = (notes_in_onset[0] + notes_in_onset[-1])/2
    for x in range(row_num_old, row_num):
        if notes_in_onset[-1] - notes_in_onset[0] <= 4: #assume only one voice
            mid_note = 60
        else: #assume two voices
            if data[row_num_old][1] <= mid_note:
                low_voice.append(data[row_num_old])
            else: 
                high_voice.append(data[row_num_old])

    
    
# print('low: ')
# print(low_voice)
# print()
# print('high: ')
# print(high_voice)


#create transition vectors
def create_transition(data_list):
    #remove instances of stacked notes in data with equal length 
    # !! needs better chord analysis
    data_short = []
    for i in range(len(data)-1):
        if not(data[i][0] == data[i+1][0] and data[i][3] == data[i+1][3]):
            data_short.append(data[i])
    #print(data_short)
    states = [] #sorted array with all possible note values
    note_val = [] #column 4 of data, sequenced note value
    for i in range(len(data)):
        note_val.append(data[i][3])
        if data[i][3] not in states:
            states.append(data[i][3])
    states.sort()
    #print(states)
    #print(note_val)
    transition = pd.crosstab(pd.Series(note_val[1:],name='succeeding note value'),
                             pd.Series(note_val[:-1],name='current note value'),normalize=1)
    print(transition)

print('high voice: ')
create_transition(high_voice)
print()
print('low voice: ')
create_transition(low_voice)
