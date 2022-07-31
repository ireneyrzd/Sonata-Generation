import numpy as np
import pandas as pd
import csv
from random import randint
from collections import Counter, OrderedDict

# F major
major = 65

# class ChordTile():
#     def __init__ (self, major):
#         self.before = major
#         self.after
        
#     chosenChord = {
#         type = 'I'
#         major = [0, 2, 4, 5, 7, 9, 11]
#     }
# }

class PredictNote: 
    major_scale = [0, 2, 4, 5, 7, 9, 11, 12] #last note?

    def __init__ (self, major, file_name):
        self.before = major
        self.after = 0
        self.chosen = 0
        self.data = []
        self.halfsteps = []
        self.orderedhalf = []
        self.file_name = file_name
    
    def preprocess(self):
        with open(self.file_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self.data.append(list(map(float, row[:-1])))


        def sub(num1,num2):
            return(num1-num2)

        def subtract(array):
            halfsteps = []
            for i in range(len(array) - 1):
                halfsteps.append(sub(self.data[i+1][1], self.data[i][1]))
            return halfsteps

        self.halfsteps = subtract(self.data)
        self.halfsteps.sort(reverse = True)
        halfdict = Counter(self.halfsteps)
        self.orderedhalf = {key:value for key, value in sorted(halfdict.items(), key=lambda item: int(item[0]), reverse = True)}

        # for key, value in orderedhalf.items():
        #     print(key, '->', value)  
     
    def find_follow(self, chords):
        sum = 0
        current_weight = 0
        #sum of weights
        for i in chords:
            sum += i[value]
        print(sum)
        n = randint(0, sum)
        print(n)
        for i in range(len(chords)):
            current_weight += chords[i][value]
            if n <= current_weight:
                follow = self.output[-1] + chords[i][value]
                return follow
                break

    def predict(self):

        num_of_notes = 12
        output = [major]

        
        for i in range(num_of_notes):
            counter = 0
            dict_short = []
            #creates array based off lead note
            for x in range(len(self.orderedhalf)):
                if output[counter] == self.orderedhalf[x]['lead']:
                    dict_short.append(self.orderedhalf[x])
            print(dict_short)
            output.append(self.find_follow(dict_short))
            counter += 1
        print(output)



n = PredictNote(major, 'higher_voice.csv')
    
        

#     -> before
#     -> next note
#     chosen = #null or 0-125
    #     possibilities =   #half steps across piano
    #     [
    #         0
    #         .
    #         .
    #         .
    #         125
    #     ]

#     observe = function(){
#         calculatePossible(){
#             look at all possible notes in adjacent note tiles
#                 for each notesThatArePlayedOnChord generate probabilities from adjacency rules and all possibble in adjacent note tiles

#         }
#     }

#     note tile = [a, b, c, d, e, f, g, h, i]