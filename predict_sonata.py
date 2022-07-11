from predict_rhythm import *
import pandas as pd
import numpy as np

rh = Predict("high_voice_transition.csv")
lh = Predict("low_voice_transition.csv",)

with open('sonata.txt', 'w') as f:
    # Exposition
    f.write('Exposition\n')

    f.write('Theme 1: \n')
    f.write('Right hand rhythm: \n')
    rh_theme1 = rh.predict(4, '1.0_1.0N')
    f.write(str(rh_theme1) + '\n') #sentence 1
    f.write(str(rh_theme1) + '\n') #setence 2

    f.write('Left hand rhythm: \n')
    lh_theme1 = lh.predict(4, '1.0_1.0R')
    f.write(str(lh_theme1) + '\n') #sentence 1
    f.write(str(lh_theme1) + '\n') #setence 2


    f.write('Bridge: \n')
    f.write('Right hand rhythm: \n')
    rh_bridge = rh.predict(4, rh.find_note(True))
    f.write(str(rh_bridge) + '\n') #bridge

    f.write('Left hand rhythm: \n')
    lh_bridge = lh.predict(4, lh.find_note(True))
    f.write(str(lh_bridge) + '\n') #bridge

    f.write('Theme 2 \n')
    f.write('Right hand rhythm: \n')
    rh_theme2 = rh.predict(4, rh.find_note(True))
    f.write(str(rh_theme2) + '\n') #sentence 1
    f.write(str(rh_theme2) + '\n') #setence 2

    f.write('Left hand rhythm: \n')
    lh_theme2 = lh.predict(4, lh.find_note(True))
    f.write(str(lh_theme2) + '\n') #sentence 1
    f.write(str(lh_theme2) + '\n') #setence 2


    # Development
    f.write('\nDevelopment\n')
    f.write('Right hand rhythm: \n')
    rh_dev = rh.predict(12, rh.find_note(True))
    f.write(str(rh_dev) + '\n') #Development

    f.write('Left hand rhythm: \n')
    lh_dev = lh.predict(12, lh.find_note(True))
    f.write(str(lh_dev) + '\n') #Development


    # Recapitulation
    f.write('\nRecapitulation\n')

    f.write('Theme 1 Recap: \n')
    f.write('Right hand rhythm: \n')
    f.write(str(rh_theme1) + '\n') #sentence 1
    f.write(str(rh_theme1) + '\n') #setence 2

    f.write('Left hand rhythm: \n')
    f.write(str(lh_theme1) + '\n') #sentence 1
    f.write(str(lh_theme1) + '\n') #setence 2


    f.write('Bridge Recap: \n')
    f.write('Right hand rhythm: \n')
    f.write(str(rh_bridge) + '\n') #bridge

    f.write('Left hand rhythm:\n ')
    f.write(str(lh_bridge) + '\n') #bridge

    f.write('Theme 2 Recap \n')
    f.write('Right hand rhythm: \n')
    f.write(str(rh_theme2) + '\n') #sentence 1
    f.write(str(rh_theme2) + '\n') #setence 2

    f.write('Left hand rhythm: \n')
    f.write(str(lh_theme2) + '\n') #sentence 1
    f.write(str(lh_theme2) + '\n') #setence 2