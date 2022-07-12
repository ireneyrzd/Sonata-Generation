
import numpy as np
import pandas as pd
import csv



#copy csv data into list data
note_data = []
with open('higher_voice.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        note_data.append(row)