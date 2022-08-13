import numpy as np
import pandas as pd
import csv
import os
from os.path import exists
import shutil

#copy csv data into list data

data = []
for i in [9, 10, 20]:
    with open('dataset/' + str(i) + '/lower_voice.csv') as csv_file: ##change
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            data.append(row)

#create transition vectors
#remove instances of stacked notes in data with equal length
data_short = []
k = 0
while k < len(data):
    #print(data[k])
    while k+1 < len(data) and data[k][-1] == 'C' and data[k+1][-1] == 'C' and float(data[k+1][0]) - float(data[k][0]) < 0.0001: #magic number to prevent float point error
        k+=1
    if (not data[k][-1] == 'R') and float(data[k][3]) == 0.0:
        k+=1
    data_short.append(data[k])
    k+=1
#print(data_short)
states = [] #sorted array with all possible note values
note_val = [] #column 4 of data, sequenced note value
for i in range(len(data_short)):
    dur = str(round(float(data_short[i][3]), 9))
    note_val.append(str(round(1+(float(data_short[i][0])%4),9)) + '_' + dur + data_short[i][6])
    #print(data_short[i][-2], note_val[i])
    if dur + data_short[i][6] not in states:
        states.append(str(round(1+(float(data_short[i][0])%4),9)) + '_' + dur + data_short[i][6])
    # print('measure', data_short[i][-2])
    # print(note_val[-1])
states.sort()
#print(note_val)
transition = pd.crosstab(pd.Series(note_val[1:],name='succeeding note value'),
                        pd.Series(note_val[:-1],name='current note value'),normalize=1)

df = pd.DataFrame(transition)
df.to_csv('low_voice_transition.csv')

# def avg_transition(name):
#     transition = []
#     states = []
#     for i in [9, 20]:
#         temp = []
#         with open('rhythm_transition/' + name  + '/' + str(i) + '_' + name + '_transition.csv') as csv_file:
#             csv_reader = csv.reader(csv_file, delimiter=',')
#             for row in csv_reader:
#                 temp = temp + row[1:]
#                 break
#         for i in range(len(temp)):
#             if temp[i] not in states:
#                 states = states + [temp[i]]
#     states.sort()
#     print(states)
#     for i in [9, 20]:
#         data = []
#         with open('rhythm_transition/' + name  + '/' + str(i) + '_' + name + '_transition.csv') as csv_file:
#             csv_reader = csv.reader(csv_file, delimiter=',')
#             for row in csv_reader:
#                 data.append(row)
#         for i in range(len(states) + 1):
#             for j in range(len(states) + 1):
#                 if i == 0 and j == 0:
#                     transition[i][j] = 0
#                 elif i == 0:
#                     transition[0][i] = states[i-1]
#                 elif j == 0:
#                     transition[j][0] = states[i-1]
#         for i in range(len(data)):
#             for j in range(len(data)):
#                 if data[i][j]
                    

                
#     for i in range(1, len(data[0])):
#         states.append(data[0][i])
#         transition.append(data[i])


            



# avg_transition('high_voice')
# avg_transition('low_voice')