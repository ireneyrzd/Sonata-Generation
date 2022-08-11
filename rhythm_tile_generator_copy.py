import numpy as np
import pandas as pd
import csv


# function create transition function for generating rhythm
def rhythm_transition():
    #copy csv data into list data
    
    data = []
    for i in range(1, 33):
        with open('dataset/' + str(i) + '/notes.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
            for row in csv_reader:
                data.append(row)

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

    #adds a row that indicates a rest
    def append_rest(arr, data, rest_duration, onset, mes):
        arr.append([str(float(onset)), '0.0', '0.0', rest_duration, str(data[4]), str(mes), 'R'])
    #splits the rests into reasonable length then append      
    def split_n_append_rest(arr, data, rest_duration, onset, mes):
        # !! needs to determine order
        if rest_duration == 1.5:
            append_rest(arr, data, '1.0', onset, mes)
            append_rest(arr, data, '0.5', str(float(onset)+1.0), mes)
        elif rest_duration == 2.5:
            append_rest(arr, data, '2.0', onset, mes)
            append_rest(arr, data, '0.5', str(float(onset)+2.0), mes)
        elif rest_duration == 3.0:
            append_rest(arr, data, '2.0', onset, mes)     
            append_rest(arr, data, '1.0', str(float(onset)+2.0), mes)
        elif rest_duration == 3.5:
            append_rest(arr, data, '2.0', onset, mes)
            append_rest(arr, data, '1.0', str(float(onset)+2.0), mes)
            append_rest(arr, data, '0.5', str(float(onset)+3.0), mes)     
        else:
            append_rest(arr, data, str(rest_duration), onset, mes)   

    #adds rests into data
    #label duration R for rest
    #label duration C for chords/interval
    #label duration N for notes
    def adds_rests(dataset, file_name):
        # !! last column not added
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
            x = i
            while dataset[x][3] == 0 and x > 0: #remove ornaments from consideration of rests
                x -= 1
            val = dataset[x]
            if val[3] == 0:
                rest_dur = dataset[i+1][0]%4
            rest_dur = dataset[i+1][0] - val[0] - val[3]
            if (dataset[i+1][0] - val[0] > 0.0001 and rest_dur > 0.0001): # magic number to dodge float point error
                #print('r')
                onset_left = 4-(val[0]+val[3])%4
                while rest_dur > onset_left:
                    # print('rest_dur' + str(rest_dur))
                    # print('onset_left' + str(onset_left))
                    mes = val[5]
                    onset = val[0] + val[3]
                    split_n_append_rest(data, dataset[i], onset_left, onset, mes)
                    rest_dur = rest_dur - onset_left
                    onset_left = 4
                    mes+=1
                    onset = (int(dataset[i][0]/4)+1)*4
                    if rest_dur <= onset_left:
                        split_n_append_rest(data, dataset[i], rest_dur, onset, mes)
                        break
                else:
                    split_n_append_rest(data, dataset[i], rest_dur, dataset[i][0] + dataset[i][3], dataset[i][5])
            # print(data[i])                          
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
        data = data_list
        #remove instances of stacked notes in data with equal length
        data_short = []
        k = 0
        while k < len(data_list):
            #print(data[k])
            while k+1 < len(data_list) and data[k][-1] == 'C' and data[k+1][-1] == 'C' and float(data[k+1][0]) - float(data[k][0]) < 0.0001: #magic number to prevent float point error
                k+=1
            if (not data[k][-1] == 'R') and float(data[k][3]) == 0.0:
                k+=1
            data_short.append(data_list[k])
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
        df.to_csv(file_name)
            # if 'high' in file_name:
            #     shutil.move(file_name, 'rhythm_transition/higher_voice/')
            # else:
            #     shutil.move(file_name, 'rhythm_transition/lower_voice/')
        return transition

    print('hi')
    create_transition(high_voice, 'high_voice_transition.csv')
    create_transition(low_voice, 'low_voice_transition.csv')

rhythm_transition()