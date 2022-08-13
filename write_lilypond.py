# Coded by Matthew Chen

from random import randint
import numpy as np
import pandas as pd
import csv
import math
def csv_to_arr(file_name):
    #copy csv data into list data
    input_data = []
    with open('output1.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            input_data.append(row)
    return input_data
data = csv_to_arr('output1.csv')
print(data)
input = ""
notes = ["c", "cis", "d", "dis", "e", "f", "fis", "g", "gis", "a", "ais", "b"]
octaves = ["", "'", "''", "'''", "''''", "'''''"]
for note in data:
    letter = ""
    octave = ""
    length = ""
    if note[5] == "N" or "C":
        index = (int(float(note[1])) - 48) % 12
        letter = notes[index]
        o_index = math.floor((int(float(note[1])) - 48) / 12)
        octave = octaves[o_index]
    if note[5] == "R":
        letter = "r"
    if float(note[2]) == 1:
            length = str(4)
    if float(note[2]) == 0.5:
            length = str(8)
    if float(note[2]) == 1.5:
            length = str("4.")
    if float(note[2]) == 2.0:
            length = str(2)
    if float(note[2]) == 3.0:
            length = str("2.")
    if float(note[2]) == 4.0:
            length = str(1)
    if (float(note[2])) == 0.25:
            length = str(1)
    if float(note[2]) == 0.333333333:
            length = str(3)
    if float(note[2]) == 0.08333:
            length = str(332)
    if float(note[2]) == 0.00834:
            length = str()
    if float(note[2]) == 1.75:
            length = str("4..")
    if float(note[2]) == 0.75:
            length = str("8.")
    #get rid of rest error here
    if note[5] == "R":
        input += letter + length + " "
    else:
        input += letter + octave + length + " "
print(input)