import numpy as np
import pandas as pd
import csv
from random import randint
from collections import Counter, OrderedDict
from predict_chord import *
from audiolazy import *
import math
import random


# find index of '_'
def find_index(str):
    index = 0
    for k in range(len(str)):
        if str[k] == '_':
            index = k
            break
    return index

def predict_note(chord_prog, rhythm, hand):
    # initialize root note:
    root = 60.0

    # initialize chord_data
    chord_data = []
    for i in [20]:
        chord_data = np.concatenate((chord_data, csv_to_arr('dataset/' + str(i) + '/chords.csv')))
  

    # initialize note_data
    file_name = 'higher_voice.csv'
    if hand == 1:
        file_name = 'lower_voice.csv'
        root = 48.0
    note_data = []
    for i in range(1, 33):
        if i == 20:
            with open('dataset/' + str(i) + '/' + file_name) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    note_data.append(row)
    k = 0
    temp=[]
    while k < len(note_data):
        #print(data[k])
        while k+1 < len(note_data) and note_data[k][-1] == 'C' and note_data[k+1][-1] == 'C' and float(note_data[k+1][0]) - float(note_data[k][0]) < 0.0001: #magic number to prevent float point error
            k+=1
        while note_data[k][-1] == 'R' or float(note_data[k][3]) == 0.0:
            k+=1
        if k < len(note_data):
            a = note_data[k]
            arr = [a[0], a[1], a[-1]]
            temp.append(arr)
        k+=1
    note_data = temp
    print(note_data)
    print(chord_data)


    # initialize a 2D array that shows where modulation happen in music
    # first col = int: measure of modulation
    # second col = string: current key
    # third col = int: midi note value of current key
    def find_mod():
        chord_data_long = []
        for i in [20]:
            with open('dataset/' + str(i) + '/chords.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    chord_data_long.append(row)
        mod = []
        mod.append([1, chord_data_long[0][2], str2midi(chord_data_long[0][2] + '4')])
        for i in range(len(chord_data_long)-1):
            if not chord_data_long[i][2] == chord_data_long[i+1][2]:
                mod.append([math.floor(float(chord_data_long[i+1][0])/4 + 1), chord_data_long[i+1][2], str2midi(chord_data_long[i+1][2] + '4')])
        return mod

    mod = find_mod()

    # print(chord_data)
    # print('mod: ', mod)



    # create a dictionary that defines the half step rule
    # key: number of half steps from the previous note (+ for going up, - for going down)
    # counter: the number of time this change in half step occurs in the corpus
    def create_hs_rule():
        def subtract(array):
            halfsteps = []
            for i in range(len(array) - 1):
                halfsteps.append(float(note_data[i+1][1]) - float(note_data[i][1]))
            return halfsteps

        halfsteps = subtract(note_data)
        halfsteps.sort(reverse = True)
        halfdict = Counter(halfsteps)
        hs_rule = {key:value for key, value in sorted(halfdict.items(), key=lambda item: int(item[0]), reverse = True)}
        # print(hs_rule)
        return hs_rule


    hs_rule = create_hs_rule()
    print('hs_rule: ', hs_rule)


    # create a nested dictionary that defines the notes that can exsist in a given chord
    # eg. dict {
    #     'I': dict{  <-- chord name
    #         '0': 5  <-- key = half step from root, val = weight
    #         '2': 9
    #     }
    #     'I42': dict{
    #        .
    #        .
    #        .
    #     }
    # }
    def create_note_rule():
        note_rule = {}
        k = 0
        j = 0
        key = mod[0][2]
        for i in range(len(chord_data)): # for each measure
            if chord_data[i] not in note_rule:
                note_rule[chord_data[i]] = {}
            while float(note_data[k][0]) < (i+1)*4 and k < len(note_data) - 1:
                # find root note
                if j < len(mod) and i > mod[j][0]:
                    key = mod[j][2]
                    j+=1
                    # print(i, key)
                # initialize note in nested array
                hs = float(note_data[k][1]) - key
                note_rule[chord_data[i]][hs] = note_rule[chord_data[i]].get(hs, 0)
                # change value
                note_rule[chord_data[i]][hs] += 1
                k+=1
        return note_rule

    note_rule = create_note_rule()
    print('note_rule: ', note_rule)

    chord_prog = chord_prog
    num_of_notes = rhythm

    # create tiles: each tile contains possible blocks/midi note value
    # a tile represent a note
    # a block represent the notes that can happen in the block given the chord
    # convert half step relation to midi note value
    # remove instance that chord doesnt allow
    tile = []
    def create_tiles():
        for i in range(len(chord_prog)):
            for j in range(num_of_notes[i]):
                note_rule[chord_prog[i]]
                midi_notes = {}
                for key in note_rule[chord_prog[i]]:
                    # if root + key >= 48.0:
                    midi_notes[root + key] = note_rule[chord_prog[i]][key]
                midi_notes = dict(sorted(midi_notes.items()))
                tile.append([chord_prog[i], midi_notes])
        print('tile', tile)
        return tile

    tile = create_tiles()
    # print('tile:', tile)


    n = 0
    def pick(index, note):
        tile[index] = note
        n = index

    def propagated(i):
        if isinstance(tile[i], int) or isinstance(tile[i], float):
            return True
        return False

    # pick a tile
    def select():
        min = 128
        # find the smallest entropy
        for i in range(len(tile)):
            if not propagated(i) and (len(tile[i]) < min):
                min = len(tile[i])
        temp = []
        # put tiles with lowest entropy into an array
        for i in range(len(tile)):    
            if not propagated(i) and (len(tile[i]) == min):    
                temp.append([i, tile[i]])
        #pick a random tile
        selected = temp[random.randint(0, len(temp) - 1)]
        # print(selected)
        return selected


    def weighted_observe(selected):
        index = selected[0]
        dict = {}
        for key in selected[1][1]:
            weight_before = 0
            if isinstance(tile[index - 1], float) or isinstance(tile[index - 1], int):
                if key - tile[index - 1] in hs_rule:
                    weight_before = hs_rule[key - tile[index - 1]]
            else:
                sum = 0
                for key2 in tile[index - 1][1]:
                    if key - key2 in hs_rule:
                        sum = sum + hs_rule[key - key2]
                weight_before = round(sum/len(tile[index - 1]))
            weight_after = 0
            if index < len(tile) - 1:
                if isinstance(tile[index + 1], float):
                    if tile[index + 1] - key in hs_rule:
                        weight_after = hs_rule[tile[index + 1] - key]
                else:
                    sum = 0
                    for key2 in tile[index + 1][1]:
                        if key2 - key in hs_rule:
                            sum = sum + hs_rule[key2 - key]
                    weight_after = round(sum/len(tile[index + 1]))
            dict[key] = round((weight_before + weight_after)/2)
        # print('dict', dict)
        # print(dict)
        tile[selected[0]] = random.choices(list(dict.keys()), weights=dict.values(), k=1)[0]
                
    # pick a random block in the selected tile
    def observe(selected):
        # print(selected)
        # print(tile)
        tile[selected[0]] = random.choice(list(selected[1][1].keys()))

    def propagate(n):
        for i in range(n+1, len(tile)):
            if not propagated(i):
                temp = {}
                for curr in tile[i][1]:
                    if not propagated(i-1):
                        for key in tile[i-1][1]:
                            if curr - key in hs_rule.keys():
                                temp[curr] = tile[i][1][curr]                        
                    else:
                        if curr - tile[i-1] in hs_rule.keys():
                            temp[curr] = tile[i][1][curr]
        for i in range(n-1, 0, -1):
            if not propagated(i):
                temp = {}
                for curr in tile[i][1]:
                    if not propagated(i+1):
                        for key in tile[i+1][1]:
                            if key - curr in hs_rule.keys():
                                temp[curr] = tile[i][1][curr]
                            
                    else:
                        if tile[i+1] - curr in hs_rule.keys():
                            temp[curr] = tile[i][1][curr]
        # print(tile)

    # check if propagation is done or if propagation has failed
    def check():
        done = True
        failed = False
        #check if propagate is done
        for i in range(len(tile)):
            if not propagated(i):
                done = False
                if len(tile[i][1]) == 0:
                    failed = True
                if len(tile[i][1]) == 1: 
                    tile[i] = list(tile[i][1]. keys())[0]
        return [done, failed]



    pick(0, root)
    propagate(0)
    while not check()[0]:
        selected = select()
        weighted_observe(selected)
        propagate(selected[0])
        if check()[1]:
            print('ERROR')
    print('tile', tile)
    return tile


# chord = ['I', 'I', 'ii6', 'V6']
# rhythm = [6, 8, 7, 6]

# predict_note(chord, rhythm, 1)

# print('selected: ', select)
# print('tiles: ', tile)
# # while not done:
# #     propagate()
# #     observe()
# #     select()

# print(tile)


        
#     return index
# index = observe()
# print(index)


# class PredictNote: 
#     chord_prog = ['I', 'V42', 'V42', 'ii6', 'V42', 'V6', 'V6', 'V42']
#     # major_chord = [0, 4, 7]
#     # minor_chord = [0, 3, 7]
#     # aug_chord = [0, 4, 8]
#     # dim_chord = [0, 3, 6]
#     # # other 7th chord?
#     # # inversiono
#     # dom_chord = [0, 4, 7, 10]
#     # major_scale = [0, 2, 4, 5, 7, 9, 11, 12] #last note?

#     def __init__ (self, major, file_name, num_of_notes):
#         self.lead = major
#         self.follow = 0
#         self.chosen = 0
#         self.data = []
#         self.halfsteps = []
#         self.file_name = file_name
#         self.weights = []
#         self.chord
#         self.chord_type = self.major_chord
#         self.inversion
#         self.num_of_notes = num_of_notes
    
#     def create_weights(self):
        
#         # for key, value in orderedhalf.items():
#         #     print(key, '->', value)  
     
#     def find_follow(self, chords):
#         sum = 0
#         current_weight = 0
#         #sum of weights
#         for i in chords:
#             sum += i[value]
#         print(sum)
#         n = randint(0, sum)
#         print(n)
#         for i in range(len(chords)):
#             current_weight += chords[i][value]
#             if n <= current_weight:
#                 follow = self.output[-1] + chords[i][value]
#                 return follow
#                 break

#     def check_chord(self, chord):
#         self.chord = chord.rstrip('0123456789')
#         self.inversion = chord[len(chord):]
#         if (self.chord[0].islower()):
#             self.chord_type = self.minor_chord 
#         if self.inversion in ('7', '65', '43', '42'):
#             self.chord_type = self.dom_chord
#         # other 7th chord??

#     def predict(self):
#         output = [major]
#         for i in range(self.num_of_notes):
#             found = False
#             while not found:
#                 self.chosen = self.find_follow(self.chord_prog[i])
#                 app_notes = self.check_chord(self.chord_prog[0])
#                 for j in range():
#                     if self.chosen%12 in app_notes:
#                         found = True
            
#             output.append(output[-1] + self.chosen)



#             # counter = 0
#             # dict_short = []
#             # #creates array based off lead note
#             # for x in range(len(self.orderedhalf)):
#             #     if output[counter] == self.orderedhalf[x]['lead']:
#             #         dict_short.append(self.orderedhalf[x])
#             # print(dict_short)
#             # output.append(self.find_follow(dict_short))
#             # counter += 1

#         print(output)



# n = PredictNote(major, 'higher_voice.csv', 12)
    
        

# #     -> before
# #     -> next note
# #     chosen = #null or 0-125
#     #     possibilities =   #half steps across piano
#     #     [
#     #         0
#     #         .
#     #         .
#     #         .
#     #         125
#     #     ]

# #     observe = function(){
# #         calculatePossible(){
# #             look at all possible notes in adjacent note tiles
# #                 for each notesThatArePlayedOnChord generate probabilities from adjacency rules and all possibble in adjacent note tiles

# #         }
# #     }

# #     note tile = [a, b, c, d, e, f, g, h, i]