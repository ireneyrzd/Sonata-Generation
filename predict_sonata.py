from predict_rhythm import *
from predict_chord import *
from predict_note import *

import pandas as pd
import numpy as np



def predict_section(mes, hand):

    n = mes #number of measures
    
    
    chord = predict_chord(n)
    if hand == 0:
        rh = Predict("high_voice_transition.csv")
        rhythm = rh.predict(n, '1.0_1.0N')
    else:
        lh = Predict("low_voice_transition.csv",)
        rhythm = lh.predict(n, '1.0_1.0N')

    notes_in_mes = []
    for i in range(n):
        notes_in_mes.append(0)
    mes = 0
    for i in range(len(rhythm) - 1):
        if not rhythm[i][:-1] == 'R':
            notes_in_mes[mes] += 1
            if rhythm[i+1][:find_index(rhythm[i+1])] < rhythm[i][:find_index(rhythm[i])]:
                mes += 1
    if not rhythm[-1][:-1] == 'R':
        notes_in_mes[-1] += 1
    # print(notes_in_mes)

    # print('chord', chord)
    notes = predict_note(chord, notes_in_mes, hand)

    print(chord)
    print(rhythm)
    print(notes)

    output = [] #[Onset, MIDI note value, note duration, RH or LH, measure number, type]
    onset = 0.0
    note_num = 0
    mes = 1
    for i in range(len(rhythm)):
        if rhythm[i][:-1] == 'R':
            output.append([onset, 0.0, float(rhythm[i][find_index(rhythm[i])+1:-1]), hand, mes, rhythm[i][:-1]])
            note_num -= 1
        else:
            output.append([onset, notes[note_num], float(rhythm[i][find_index(rhythm[i])+1:-1]), hand, mes, rhythm[i][-1:]])
        if output[-1][-1] == 'C':
            output.append([onset, notes[note_num] - 4, float(rhythm[i][find_index(rhythm[i])+1:-1]), hand, mes, rhythm[i][-1:]]) # M3 down
        #update note_num
        note_num += 1
        #update mes num
        if i < len(rhythm) - 1:
            if rhythm[i+1][:find_index(rhythm[i+1])] < rhythm[i][:find_index(rhythm[i])]:
                mes += 1
        #update onset
        onset += round(float(rhythm[i][find_index(rhythm[i])+1:-1]), 9)
        onset = round(onset, 9)
        if str(onset)[-1] == '9':
            onset += 0.000000001
        #print(onset)

    print(output)

    with open('output' + str(hand) +'.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows(output)

predict_section(16, 0)
predict_section(16, 1)



# with open('sonata.txt', 'w') as f:
#     # Exposition
#     f.write('Exposition\n')

#     f.write('Theme 1: \n')
#     f.write('Right hand rhythm: \n')
#     rh_theme1 = rh.predict(4, '1.0_1.0N')
#     print(rh_theme1)
#     f.write(str(rh_theme1) + '\n') #sentence 1
#     f.write(str(rh_theme1) + '\n') #setence 2

#     f.write('Left hand rhythm: \n')
#     lh_theme1 = lh.predict(4, '1.0_1.0R')
#     f.write(str(lh_theme1) + '\n') #sentence 1
#     f.write(str(lh_theme1) + '\n') #setence 2


#     f.write('Bridge: \n')
#     f.write('Right hand rhythm: \n')
#     rh_bridge = rh.predict(4, rh.find_note(True))
#     f.write(str(rh_bridge) + '\n') #bridge

#     f.write('Left hand rhythm: \n')
#     lh_bridge = lh.predict(4, lh.find_note(True))
#     f.write(str(lh_bridge) + '\n') #bridge

#     f.write('Theme 2 \n')
#     f.write('Right hand rhythm: \n')
#     rh_theme2 = rh.predict(4, rh.find_note(True))
#     f.write(str(rh_theme2) + '\n') #sentence 1
#     f.write(str(rh_theme2) + '\n') #setence 2

#     f.write('Left hand rhythm: \n')
#     lh_theme2 = lh.predict(4, lh.find_note(True))
#     f.write(str(lh_theme2) + '\n') #sentence 1
#     f.write(str(lh_theme2) + '\n') #setence 2


#     # Development
#     f.write('\nDevelopment\n')
#     f.write('Right hand rhythm: \n')
#     rh_dev = rh.predict(12, rh.find_note(True))
#     f.write(str(rh_dev) + '\n') #Development

#     f.write('Left hand rhythm: \n')
#     lh_dev = lh.predict(12, lh.find_note(True))
#     f.write(str(lh_dev) + '\n') #Development


#     # Recapitulation
#     f.write('\nRecapitulation\n')

#     f.write('Theme 1 Recap: \n')
#     f.write('Right hand rhythm: \n')
#     f.write(str(rh_theme1) + '\n') #sentence  
#     f.write(str(rh_theme1) + '\n') #setence 2

#     f.write('Left hand rhythm: \n')
#     f.write(str(lh_theme1) + '\n') #sentence 1
#     f.write(str(lh_theme1) + '\n') #setence 2


#     f.write('Bridge Recap: \n')
#     f.write('Right hand rhythm: \n')
#     f.write(str(rh_bridge) + '\n') #bridge

#     f.write('Left hand rhythm:\n ')
#     f.write(str(lh_bridge) + '\n') #bridge

#     f.write('Theme 2 Recap \n')
#     f.write('Right hand rhythm: \n')
#     f.write(str(rh_theme2) + '\n') #sentence 1
#     f.write(str(rh_theme2) + '\n') #setence 2

#     f.write('Left hand rhythm: \n')
#     f.write(str(lh_theme2) + '\n') #sentence 1
#     f.write(str(lh_theme2) + '\n') #setence 2