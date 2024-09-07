import numpy as np
import pandas as pd
import xlrd
import csv
from random import randrange
import os
import glob
pd.options.mode.chained_assignment = None  # default='warn'

#load in all the houses at once
path = os.getcwd()
csv_files = glob.glob(os.path.join(path, "*.csv"))
#put all these .csv house data files into a dictionary
house_input_dict = {}
for i, f in zip(range(84), csv_files):
    df = pd.read_csv(f)
    x = f.split("\\")[-1]
    id = x.split(".")[0]
    new = {id:df}
    house_input_dict.update(new)


#global variables
weeks = 4 #number of weeks for the simulation to run
ElecTariff=75 # <20=economy, >20=standard
SoC100 = 37 #kWh
SoC20 = 7.4 #kWh JUST CHANGE THIS TO CHANGE THE LOWER THRESHOLD WHICH INITIATES A CHARGING EVENT
#FOR CHARGING EVERY NIGHT, SET THIS TO 80% (29.6)
SoC80 = 29.6 #kWh

#THE BIG FOR LOOP
for house in house_input_dict.keys():
    HouseData = house_input_dict[house]
    #print('Data for', house, 'loaded in')
    #print(HouseData)




    #Data Pre-Processing Stage
    # All the possible column headings needed
    Car1headings = ['Time','Car 1 Mon Location', 'Car 1 Mon Location Code', 'Car 1 Mon Miles', 'Car 1 Mon Energy', 'Car 1 Tue Location', 'Car 1 Tue Location Code', 'Car 1 Tue Miles', 'Car 1 Tue Energy', 'Car 1 Wed Location', 'Car 1 Wed Location Code', 'Car 1 Wed Miles', 'Car 1 Wed Energy', 'Car 1 Thurs Location', 'Car 1 Thurs Location Code', 'Car 1 Thurs Miles', 'Car 1 Thurs Energy', 'Car 1 Fri Location', 'Car 1 Fri Location Code', 'Car 1 Fri Miles', 'Car 1 Fri Energy', 'Car 1 Sat Location', 'Car 1 Sat Location Code', 'Car 1 Sat Miles', 'Car 1 Sat Energy', 'Car 1 Sun Location', 'Car 1 Sun Location Code', 'Car 1 Sun Miles', 'Car 1 Sun Energy',]
    Car2headings = ['Time1', 'Car 2 Mon Location', 'Car 2 Mon Location Code', 'Car 2 Mon Miles', 'Car 2 Mon Energy', 'Car 2 Tue Location', 'Car 2 Tue Location Code', 'Car 2 Tue Miles', 'Car 2 Tue Energy', 'Car 2 Wed Location', 'Car 2 Wed Location Code', 'Car 2 Wed Miles', 'Car 2 Wed Energy', 'Car 2 Thurs Location', 'Car 2 Thurs Location Code', 'Car 2 Thurs Miles', 'Car 2 Thurs Energy', 'Car 2 Fri Location', 'Car 2 Fri Location Code', 'Car 2 Fri Miles', 'Car 2 Fri Energy', 'Car 2 Sat Location', 'Car 2 Sat Location Code', 'Car 2 Sat Miles', 'Car 2 Sat Energy', 'Car 2 Sun Location', 'Car 2 Sun Location Code', 'Car 2 Sun Miles', 'Car 2 Sun Energy',]
    Car3headings = ['Time2', 'Car 3 Mon Location', 'Car 3 Mon Location Code', 'Car 3 Mon Miles', 'Car 3 Mon Energy', 'Car 3 Tue Location', 'Car 3 Tue Location Code', 'Car 3 Tue Miles', 'Car 3 Tue Energy', 'Car 3 Wed Location', 'Car 3 Wed Location Code', 'Car 3 Wed Miles', 'Car 3 Wed Energy', 'Car 3 Thurs Location', 'Car 3 Thurs Location Code', 'Car 3 Thurs Miles', 'Car 3 Thurs Energy', 'Car 3 Fri Location', 'Car 3 Fri Location Code', 'Car 3 Fri Miles', 'Car 3 Fri Energy', 'Car 3 Sat Location', 'Car 3 Sat Location Code', 'Car 3 Sat Miles', 'Car 3 Sat Energy', 'Car 3 Sun Location', 'Car 3 Sun Location Code', 'Car 3 Sun Miles', 'Car 3 Sun Energy',]
    Car4headings = ['Time3', 'Car 4 Mon Location', 'Car 4 Mon Location Code', 'Car 4 Mon Miles', 'Car 4 Mon Energy', 'Car 4 Tue Location', 'Car 4 Tue Location Code', 'Car 4 Tue Miles', 'Car 4 Tue Energy', 'Car 4 Wed Location', 'Car 4 Wed Location Code', 'Car 4 Wed Miles', 'Car 4 Wed Energy', 'Car 4 Thurs Location', 'Car 4 Thurs Location Code', 'Car 4 Thurs Miles', 'Car 4 Thurs Energy', 'Car 4 Fri Location', 'Car 4 Fri Location Code', 'Car 4 Fri Miles', 'Car 4 Fri Energy', 'Car 4 Sat Location', 'Car 4 Sat Location Code', 'Car 4 Sat Miles', 'Car 4 Sat Energy', 'Car 4 Sun Location', 'Car 4 Sun Location Code', 'Car 4 Sun Miles', 'Car 4 Sun Energy',]
    column_names = Car1headings + Car2headings + Car3headings + Car4headings

    # ==============================================================================
    # Converts Imported Dataframe into dataframe with correct headings for use going forward
    num_cols = len(HouseData.columns)
    #print(num_cols)
    #1 car = 29 columns
    #2 cars = 58 columns
    #3 cars = 87 columns
    #4 cars = 116 columns
    HouseData2 = pd.DataFrame(HouseData[1:])

    if num_cols == 29: #one car
        HouseData2.columns = column_names[0:29]
    elif num_cols == 29*2: #two cars
        HouseData2.columns = column_names[0:58]
        HouseData2 = HouseData2.drop(["Time1"], axis=1) #dropping the additional time column
    elif num_cols == 29*3: #three cars
        HouseData2.columns = column_names[0:87]
        HouseData2 = HouseData2.drop(["Time1", "Time2"], axis=1) #dropping the additional time columns
    elif num_cols == 29*4: #four cars
        HouseData2.columns = column_names
        HouseData2 = HouseData2.drop(["Time1", "Time2", "Time3"], axis=1) #dropping the additional time columns
    else:
        print('There shouldnt be this many columns...')


    # ==============================================================================
    # Now to add the Day 0 Columns (each Car will repeats its Day 1)


    if num_cols == 29: #one car
        HouseData2.insert(1, "Car 1 Day 0 Location", HouseData2['Car 1 Mon Location'])
        HouseData2.insert(2, "Car 1 Day 0 Location Code", HouseData2['Car 1 Mon Location Code'])
        HouseData2.insert(3, "Car 1 Day 0 Miles", HouseData2['Car 1 Mon Miles'])
        HouseData2.insert(4, "Car 1 Day 0 Energy", HouseData2['Car 1 Mon Energy'])

    elif num_cols == 29*2: #two car
        HouseData2.insert(1, "Car 1 Day 0 Location", HouseData2['Car 1 Mon Location'])
        HouseData2.insert(2, "Car 1 Day 0 Location Code", HouseData2['Car 1 Mon Location Code'])
        HouseData2.insert(3, "Car 1 Day 0 Miles", HouseData2['Car 1 Mon Miles'])
        HouseData2.insert(4, "Car 1 Day 0 Energy", HouseData2['Car 1 Mon Energy'])

        HouseData2.insert(33, "Car 2 Day 0 Location", HouseData2['Car 2 Mon Location'])
        HouseData2.insert(34, "Car 2 Day 0 Location Code", HouseData2['Car 2 Mon Location Code'])
        HouseData2.insert(35, "Car 2 Day 0 Miles", HouseData2['Car 2 Mon Miles'])
        HouseData2.insert(36, "Car 2 Day 0 Energy", HouseData2['Car 2 Mon Energy'])

    elif num_cols == 29*3: #three car
        HouseData2.insert(1, "Car 1 Day 0 Location", HouseData2['Car 1 Mon Location'])
        HouseData2.insert(2, "Car 1 Day 0 Location Code", HouseData2['Car 1 Mon Location Code'])
        HouseData2.insert(3, "Car 1 Day 0 Miles", HouseData2['Car 1 Mon Miles'])
        HouseData2.insert(4, "Car 1 Day 0 Energy", HouseData2['Car 1 Mon Energy'])

        HouseData2.insert(33, "Car 2 Day 0 Location", HouseData2['Car 2 Mon Location'])
        HouseData2.insert(34, "Car 2 Day 0 Location Code", HouseData2['Car 2 Mon Location Code'])
        HouseData2.insert(35, "Car 2 Day 0 Miles", HouseData2['Car 2 Mon Miles'])
        HouseData2.insert(36, "Car 2 Day 0 Energy", HouseData2['Car 2 Mon Energy'])

        HouseData2.insert(65, "Car 3 Day 0 Location", HouseData2['Car 3 Mon Location'])
        HouseData2.insert(66, "Car 3 Day 0 Location Code", HouseData2['Car 3 Mon Location Code'])
        HouseData2.insert(67, "Car 3 Day 0 Miles", HouseData2['Car 3 Mon Miles'])
        HouseData2.insert(68, "Car 3 Day 0 Energy", HouseData2['Car 3 Mon Energy'])

    elif num_cols == 29*4: #four car
        HouseData2.insert(1, "Car 1 Day 0 Location", HouseData2['Car 1 Mon Location'])
        HouseData2.insert(2, "Car 1 Day 0 Location Code", HouseData2['Car 1 Mon Location Code'])
        HouseData2.insert(3, "Car 1 Day 0 Miles", HouseData2['Car 1 Mon Miles'])
        HouseData2.insert(4, "Car 1 Day 0 Energy", HouseData2['Car 1 Mon Energy'])

        HouseData2.insert(33, "Car 2 Day 0 Location", HouseData2['Car 2 Mon Location'])
        HouseData2.insert(34, "Car 2 Day 0 Location Code", HouseData2['Car 2 Mon Location Code'])
        HouseData2.insert(35, "Car 2 Day 0 Miles", HouseData2['Car 2 Mon Miles'])
        HouseData2.insert(36, "Car 2 Day 0 Energy", HouseData2['Car 2 Mon Energy'])

        HouseData2.insert(65, "Car 3 Day 0 Location", HouseData2['Car 3 Mon Location'])
        HouseData2.insert(66, "Car 3 Day 0 Location Code", HouseData2['Car 3 Mon Location Code'])
        HouseData2.insert(67, "Car 3 Day 0 Miles", HouseData2['Car 3 Mon Miles'])
        HouseData2.insert(68, "Car 3 Day 0 Energy", HouseData2['Car 3 Mon Energy'])

        HouseData2.insert(97, "Car 4 Day 0 Location", HouseData2['Car 4 Mon Location'])
        HouseData2.insert(98, "Car 4 Day 0 Location Code", HouseData2['Car 4 Mon Location Code'])
        HouseData2.insert(99, "Car 4 Day 0 Miles", HouseData2['Car 4 Mon Miles'])
        HouseData2.insert(100, "Car 4 Day 0 Energy", HouseData2['Car 4 Mon Energy'])

    else:
        print('There shouldnt be this many columns...')


    # ==============================================================================
    #Energy Calculation in HouseData
    #Nissan Leaf consumption rate = 26.5 kWh/100mile
    LeafConsump = 26.5/100

    #searches for all the columns with the word 'Energy' in
    energy_cols=[col for col in HouseData2.columns if 'Energy' in col]

    #searches for all the columns with the word 'Miles' in
    miles_cols=[col for col in HouseData2.columns if 'Miles' in col]

    for i, j in zip(energy_cols, miles_cols):
        HouseData2[i] = LeafConsump * HouseData2[j].astype(str).astype(float)




    #CHARGING!!!!
    #Need to add Charging Columns
    #adding empty columns to be filled with the energy charged back onto the cars

    if num_cols == 29: #one car
        HouseData2.insert(5, "Car 1 Day 0 Charging Energy", np.NaN)
        HouseData2.insert(10, "Car 1 Mon Charging Energy", np.NaN)
        HouseData2.insert(15, "Car 1 Tue Charging Energy", np.NaN)
        HouseData2.insert(20, "Car 1 Wed Charging Energy", np.NaN)
        HouseData2.insert(25, "Car 1 Thurs Charging Energy", np.NaN)
        HouseData2.insert(30, "Car 1 Fri Charging Energy", np.NaN)
        HouseData2.insert(35, "Car 1 Sat Charging Energy", np.NaN)
        HouseData2.insert(40, "Car 1 Sun Charging Energy", np.NaN)

    elif num_cols == 29*2: #two car
        HouseData2.insert(5, "Car 1 Day 0 Charging Energy", np.NaN)
        HouseData2.insert(10, "Car 1 Mon Charging Energy", np.NaN)
        HouseData2.insert(15, "Car 1 Tue Charging Energy", np.NaN)
        HouseData2.insert(20, "Car 1 Wed Charging Energy", np.NaN)
        HouseData2.insert(25, "Car 1 Thurs Charging Energy", np.NaN)
        HouseData2.insert(30, "Car 1 Fri Charging Energy", np.NaN)
        HouseData2.insert(35, "Car 1 Sat Charging Energy", np.NaN)
        HouseData2.insert(40, "Car 1 Sun Charging Energy", np.NaN)

        HouseData2.insert(45, "Car 2 Day 0 Charging Energy", np.NaN)
        HouseData2.insert(50, "Car 2 Mon Charging Energy", np.NaN)
        HouseData2.insert(55, "Car 2 Tue Charging Energy", np.NaN)
        HouseData2.insert(60, "Car 2 Wed Charging Energy", np.NaN)
        HouseData2.insert(65, "Car 2 Thurs Charging Energy", np.NaN)
        HouseData2.insert(70, "Car 2 Fri Charging Energy", np.NaN)
        HouseData2.insert(75, "Car 2 Sat Charging Energy", np.NaN)
        HouseData2.insert(80, "Car 2 Sun Charging Energy", np.NaN)

    elif num_cols == 29*3: #three car
        HouseData2.insert(5, "Car 1 Day 0 Charging Energy", np.NaN)
        HouseData2.insert(10, "Car 1 Mon Charging Energy", np.NaN)
        HouseData2.insert(15, "Car 1 Tue Charging Energy", np.NaN)
        HouseData2.insert(20, "Car 1 Wed Charging Energy", np.NaN)
        HouseData2.insert(25, "Car 1 Thurs Charging Energy", np.NaN)
        HouseData2.insert(30, "Car 1 Fri Charging Energy", np.NaN)
        HouseData2.insert(35, "Car 1 Sat Charging Energy", np.NaN)
        HouseData2.insert(40, "Car 1 Sun Charging Energy", np.NaN)

        HouseData2.insert(45, "Car 2 Day 0 Charging Energy", np.NaN)
        HouseData2.insert(50, "Car 2 Mon Charging Energy", np.NaN)
        HouseData2.insert(55, "Car 2 Tue Charging Energy", np.NaN)
        HouseData2.insert(60, "Car 2 Wed Charging Energy", np.NaN)
        HouseData2.insert(65, "Car 2 Thurs Charging Energy", np.NaN)
        HouseData2.insert(70, "Car 2 Fri Charging Energy", np.NaN)
        HouseData2.insert(75, "Car 2 Sat Charging Energy", np.NaN)
        HouseData2.insert(80, "Car 2 Sun Charging Energy", np.NaN)

        HouseData2.insert(85, "Car 3 Day 0 Charging Energy", np.NaN)
        HouseData2.insert(90, "Car 3 Mon Charging Energy", np.NaN)
        HouseData2.insert(95, "Car 3 Tue Charging Energy", np.NaN)
        HouseData2.insert(100, "Car 3 Wed Charging Energy", np.NaN)
        HouseData2.insert(105, "Car 3 Thurs Charging Energy", np.NaN)
        HouseData2.insert(110, "Car 3 Fri Charging Energy", np.NaN)
        HouseData2.insert(115, "Car 3 Sat Charging Energy", np.NaN)
        HouseData2.insert(120, "Car 3 Sun Charging Energy", np.NaN)

    elif num_cols == 29*4: #four car
        HouseData2.insert(5, "Car 1 Day 0 Charging Energy", np.NaN)
        HouseData2.insert(10, "Car 1 Mon Charging Energy", np.NaN)
        HouseData2.insert(15, "Car 1 Tue Charging Energy", np.NaN)
        HouseData2.insert(20, "Car 1 Wed Charging Energy", np.NaN)
        HouseData2.insert(25, "Car 1 Thurs Charging Energy", np.NaN)
        HouseData2.insert(30, "Car 1 Fri Charging Energy", np.NaN)
        HouseData2.insert(35, "Car 1 Sat Charging Energy", np.NaN)
        HouseData2.insert(40, "Car 1 Sun Charging Energy", np.NaN)

        HouseData2.insert(45, "Car 2 Day 0 Charging Energy", np.NaN)
        HouseData2.insert(50, "Car 2 Mon Charging Energy", np.NaN)
        HouseData2.insert(55, "Car 2 Tue Charging Energy", np.NaN)
        HouseData2.insert(60, "Car 2 Wed Charging Energy", np.NaN)
        HouseData2.insert(65, "Car 2 Thurs Charging Energy", np.NaN)
        HouseData2.insert(70, "Car 2 Fri Charging Energy", np.NaN)
        HouseData2.insert(75, "Car 2 Sat Charging Energy", np.NaN)
        HouseData2.insert(80, "Car 2 Sun Charging Energy", np.NaN)

        HouseData2.insert(85, "Car 3 Day 0 Charging Energy", np.NaN)
        HouseData2.insert(90, "Car 3 Mon Charging Energy", np.NaN)
        HouseData2.insert(95, "Car 3 Tue Charging Energy", np.NaN)
        HouseData2.insert(100, "Car 3 Wed Charging Energy", np.NaN)
        HouseData2.insert(105, "Car 3 Thurs Charging Energy", np.NaN)
        HouseData2.insert(110, "Car 3 Fri Charging Energy", np.NaN)
        HouseData2.insert(115, "Car 3 Sat Charging Energy", np.NaN)
        HouseData2.insert(120, "Car 3 Sun Charging Energy", np.NaN)

        HouseData2.insert(125, "Car 4 Day 0 Charging Energy", np.NaN)
        HouseData2.insert(130, "Car 4 Mon Charging Energy", np.NaN)
        HouseData2.insert(135, "Car 4 Tue Charging Energy", np.NaN)
        HouseData2.insert(140, "Car 4 Wed Charging Energy", np.NaN)
        HouseData2.insert(145, "Car 4 Thurs Charging Energy", np.NaN)
        HouseData2.insert(150, "Car 4 Fri Charging Energy", np.NaN)
        HouseData2.insert(155, "Car 4 Sat Charging Energy", np.NaN)
        HouseData2.insert(160, "Car 4 Sun Charging Energy", np.NaN)

    else:
        print('There shouldnt be this many columns...')


    #Need to Add Battery Capacity Columns
    #adding empty columns to be filled with battery capacity through the day, taking
    #into account the discharge and charge at each time interval

    if num_cols == 29: #one car
        HouseData2.insert(5, "Car 1 Day 0 Battery Capacity", np.NaN)
        HouseData2.insert(11, "Car 1 Mon Battery Capacity", np.NaN)
        HouseData2.insert(17, "Car 1 Tue Battery Capacity", np.NaN)
        HouseData2.insert(23, "Car 1 Wed Battery Capacity", np.NaN)
        HouseData2.insert(29, "Car 1 Thurs Battery Capacity", np.NaN)
        HouseData2.insert(35, "Car 1 Fri Battery Capacity", np.NaN)
        HouseData2.insert(41, "Car 1 Sat Battery Capacity", np.NaN)
        HouseData2.insert(47, "Car 1 Sun Battery Capacity", np.NaN)

    elif num_cols == 29*2: #two car
        HouseData2.insert(5, "Car 1 Day 0 Battery Capacity", np.NaN)
        HouseData2.insert(11, "Car 1 Mon Battery Capacity", np.NaN)
        HouseData2.insert(17, "Car 1 Tue Battery Capacity", np.NaN)
        HouseData2.insert(23, "Car 1 Wed Battery Capacity", np.NaN)
        HouseData2.insert(29, "Car 1 Thurs Battery Capacity", np.NaN)
        HouseData2.insert(35, "Car 1 Fri Battery Capacity", np.NaN)
        HouseData2.insert(41, "Car 1 Sat Battery Capacity", np.NaN)
        HouseData2.insert(47, "Car 1 Sun Battery Capacity", np.NaN)

        HouseData2.insert(53, "Car 2 Day 0 Battery Capacity", np.NaN)
        HouseData2.insert(59, "Car 2 Mon Battery Capacity", np.NaN)
        HouseData2.insert(65, "Car 2 Tue Battery Capacity", np.NaN)
        HouseData2.insert(71, "Car 2 Wed Battery Capacity", np.NaN)
        HouseData2.insert(77, "Car 2 Thurs Battery Capacity", np.NaN)
        HouseData2.insert(83, "Car 2 Fri Battery Capacity", np.NaN)
        HouseData2.insert(89, "Car 2 Sat Battery Capacity", np.NaN)
        HouseData2.insert(95, "Car 2 Sun Battery Capacity", np.NaN)

    elif num_cols == 29*3: #three car
        HouseData2.insert(5, "Car 1 Day 0 Battery Capacity", np.NaN)
        HouseData2.insert(11, "Car 1 Mon Battery Capacity", np.NaN)
        HouseData2.insert(17, "Car 1 Tue Battery Capacity", np.NaN)
        HouseData2.insert(23, "Car 1 Wed Battery Capacity", np.NaN)
        HouseData2.insert(29, "Car 1 Thurs Battery Capacity", np.NaN)
        HouseData2.insert(35, "Car 1 Fri Battery Capacity", np.NaN)
        HouseData2.insert(41, "Car 1 Sat Battery Capacity", np.NaN)
        HouseData2.insert(47, "Car 1 Sun Battery Capacity", np.NaN)

        HouseData2.insert(53, "Car 2 Day 0 Battery Capacity", np.NaN)
        HouseData2.insert(59, "Car 2 Mon Battery Capacity", np.NaN)
        HouseData2.insert(65, "Car 2 Tue Battery Capacity", np.NaN)
        HouseData2.insert(71, "Car 2 Wed Battery Capacity", np.NaN)
        HouseData2.insert(77, "Car 2 Thurs Battery Capacity", np.NaN)
        HouseData2.insert(83, "Car 2 Fri Battery Capacity", np.NaN)
        HouseData2.insert(89, "Car 2 Sat Battery Capacity", np.NaN)
        HouseData2.insert(95, "Car 2 Sun Battery Capacity", np.NaN)

        HouseData2.insert(101, "Car 3 Day 0 Battery Capacity", np.NaN)
        HouseData2.insert(107, "Car 3 Mon Battery Capacity", np.NaN)
        HouseData2.insert(113, "Car 3 Tue Battery Capacity", np.NaN)
        HouseData2.insert(119, "Car 3 Wed Battery Capacity", np.NaN)
        HouseData2.insert(125, "Car 3 Thurs Battery Capacity", np.NaN)
        HouseData2.insert(131, "Car 3 Fri Battery Capacity", np.NaN)
        HouseData2.insert(137, "Car 3 Sat Battery Capacity", np.NaN)
        HouseData2.insert(143, "Car 3 Sun Battery Capacity", np.NaN)

    elif num_cols == 29*4: #four car
        HouseData2.insert(5, "Car 1 Day 0 Battery Capacity", np.NaN)
        HouseData2.insert(11, "Car 1 Mon Battery Capacity", np.NaN)
        HouseData2.insert(17, "Car 1 Tue Battery Capacity", np.NaN)
        HouseData2.insert(23, "Car 1 Wed Battery Capacity", np.NaN)
        HouseData2.insert(29, "Car 1 Thurs Battery Capacity", np.NaN)
        HouseData2.insert(35, "Car 1 Fri Battery Capacity", np.NaN)
        HouseData2.insert(41, "Car 1 Sat Battery Capacity", np.NaN)
        HouseData2.insert(47, "Car 1 Sun Battery Capacity", np.NaN)

        HouseData2.insert(53, "Car 2 Day 0 Battery Capacity", np.NaN)
        HouseData2.insert(59, "Car 2 Mon Battery Capacity", np.NaN)
        HouseData2.insert(65, "Car 2 Tue Battery Capacity", np.NaN)
        HouseData2.insert(71, "Car 2 Wed Battery Capacity", np.NaN)
        HouseData2.insert(77, "Car 2 Thurs Battery Capacity", np.NaN)
        HouseData2.insert(83, "Car 2 Fri Battery Capacity", np.NaN)
        HouseData2.insert(89, "Car 2 Sat Battery Capacity", np.NaN)
        HouseData2.insert(95, "Car 2 Sun Battery Capacity", np.NaN)

        HouseData2.insert(101, "Car 3 Day 0 Battery Capacity", np.NaN)
        HouseData2.insert(107, "Car 3 Mon Battery Capacity", np.NaN)
        HouseData2.insert(113, "Car 3 Tue Battery Capacity", np.NaN)
        HouseData2.insert(119, "Car 3 Wed Battery Capacity", np.NaN)
        HouseData2.insert(125, "Car 3 Thurs Battery Capacity", np.NaN)
        HouseData2.insert(131, "Car 3 Fri Battery Capacity", np.NaN)
        HouseData2.insert(137, "Car 3 Sat Battery Capacity", np.NaN)
        HouseData2.insert(143, "Car 3 Sun Battery Capacity", np.NaN)

        HouseData2.insert(149, "Car 4 Day 0 Battery Capacity", np.NaN)
        HouseData2.insert(155, "Car 4 Mon Battery Capacity", np.NaN)
        HouseData2.insert(161, "Car 4 Tue Battery Capacity", np.NaN)
        HouseData2.insert(167, "Car 4 Wed Battery Capacity", np.NaN)
        HouseData2.insert(173, "Car 4 Thurs Battery Capacity", np.NaN)
        HouseData2.insert(179, "Car 4 Fri Battery Capacity", np.NaN)
        HouseData2.insert(185, "Car 4 Sat Battery Capacity", np.NaN)
        HouseData2.insert(191, "Car 4 Sun Battery Capacity", np.NaN)

    else:
        print('There shouldnt be this many columns...')

    #THE METHOD FOR GETTING AROUND MULTIPLE CARS AT A HOUSEHOLD, FOR THE CASE WHEN THERE IS A CHARGER PER CAR IS
    #TO USE A DICTIONARY OF DATAFRAMES, WHERE EACH KEY IS A CAR AND THE VALUE ATTACHED TO THAT KEY IS THE DATAFRAME

    #TRANSFORMING HOUSEDATA2 INTO A DICTIONARY
    HouseData3 = {}
    #Making the dictionary of dataframes
    if num_cols == 29: #one car
        HouseData3['Car 1'] = pd.DataFrame(data = HouseData2)
    elif num_cols == 29*2: #two cars
        HouseData3['Car 1'] = pd.DataFrame(data = HouseData2.iloc[:, 0:49])
        HouseData3['Car 2'] = pd.DataFrame(data = HouseData2.iloc[:, -48:])
        HouseData3['Car 2'].insert(0, 'Time', HouseData2.iloc[:,0]) #Adding the time column
    elif num_cols == 29*3: #three cars
        HouseData3['Car 1'] = pd.DataFrame(data = HouseData2.iloc[:, 0:49])
        HouseData3['Car 2'] = pd.DataFrame(data = HouseData2.iloc[:, 49:97])
        HouseData3['Car 3'] = pd.DataFrame(data = HouseData2.iloc[:, -48:])
        HouseData3['Car 2'].insert(0, 'Time', HouseData2.iloc[:,0]) #Adding the time column
        HouseData3['Car 3'].insert(0, 'Time', HouseData2.iloc[:,0]) #Adding the time column
    elif num_cols == 29*4: #four cars
        HouseData3['Car 1'] = pd.DataFrame(data = HouseData2.iloc[:, 0:49])
        HouseData3['Car 2'] = pd.DataFrame(data = HouseData2.iloc[:, 49:97])
        HouseData3['Car 3'] = pd.DataFrame(data = HouseData2.iloc[:, 97:145])
        HouseData3['Car 4'] = pd.DataFrame(data = HouseData2.iloc[:, -48:])
        HouseData3['Car 2'].insert(0, 'Time', HouseData2.iloc[:,0]) #Adding the time column
        HouseData3['Car 3'].insert(0, 'Time', HouseData2.iloc[:,0]) #Adding the time column
        HouseData3['Car 4'].insert(0, 'Time', HouseData2.iloc[:,0]) #Adding the time column
    else:
        print('There shouldnt be this many cars...')


    #Now need to get rid of the 'Car No.' in each heading, so as the below code doesnt need to be changed
    if num_cols == 29: #one car
        HouseData3['Car 1'].columns = HouseData3['Car 1'].columns.str.replace('^Car 1 ','')
    elif num_cols == 29*2: #two cars
        HouseData3['Car 1'].columns = HouseData3['Car 1'].columns.str.replace('^Car 1 ','')
        HouseData3['Car 2'].columns = HouseData3['Car 2'].columns.str.replace('^Car 2 ','')
    elif num_cols == 29*3: #three cars
        HouseData3['Car 1'].columns = HouseData3['Car 1'].columns.str.replace('^Car 1 ','')
        HouseData3['Car 2'].columns = HouseData3['Car 2'].columns.str.replace('^Car 2 ','')
        HouseData3['Car 3'].columns = HouseData3['Car 3'].columns.str.replace('^Car 3 ','')
    elif num_cols == 29*4: #four cars
        HouseData3['Car 1'].columns = HouseData3['Car 1'].columns.str.replace('^Car 1 ','')
        HouseData3['Car 2'].columns = HouseData3['Car 2'].columns.str.replace('^Car 2 ','')
        HouseData3['Car 3'].columns = HouseData3['Car 3'].columns.str.replace('^Car 3 ','')
        HouseData3['Car 4'].columns = HouseData3['Car 4'].columns.str.replace('^Car 4 ','')
    else:
        print('There shouldnt be this many cars...')

    #Making the car list
    if num_cols == 29: #one car
        car_list = ['Car 1']
    elif num_cols == 29*2: #two cars
        car_list = ['Car 1', 'Car 2']
    elif num_cols == 29*3: #three cars
        car_list = ['Car 1', 'Car 2', 'Car 3']
    elif num_cols == 29*4: #four cars
        car_list = ['Car 1', 'Car 2', 'Car 3', 'Car 4']
    else:
        print('There shouldnt be this many cars...')

    #making list of headings (apart from Time and Location (the word one))
    headings = list(HouseData3['Car 1'].columns)
    headings.remove('Time')
    headings.remove('Day 0 Location')
    headings.remove('Mon Location')
    headings.remove('Tue Location')
    headings.remove('Wed Location')
    headings.remove('Thurs Location')
    headings.remove('Fri Location')
    headings.remove('Sat Location')
    headings.remove('Sun Location')

    #converting the number values of the dataframe to float values
    for car in car_list:
        for x in headings:
                HouseData3[car][x] = HouseData3[car][x].astype(float)

    for car in car_list:
        HouseData3[car] = HouseData3[car].reset_index(drop=True)

    #Add in the power columns of the charger (6.6kW) and power used
    for x in car_list:
        HouseData3[x].insert(7, "Day 0 Charging Power", np.NaN)
        HouseData3[x].insert(14, "Mon Charging Power", np.NaN)
        HouseData3[x].insert(21, "Tue Charging Power", np.NaN)
        HouseData3[x].insert(28, "Wed Charging Power", np.NaN)
        HouseData3[x].insert(35, "Thurs Charging Power", np.NaN)
        HouseData3[x].insert(42, "Fri Charging Power", np.NaN)
        HouseData3[x].insert(49, "Sat Charging Power", np.NaN)
        HouseData3[x].insert(56, "Sun Charging Power", np.NaN)

    #State of Charge (SoC) Calculation
    for x in car_list:
        HouseData3[x].insert(8, "Day 0 State of Charge (%)", np.NaN)
        HouseData3[x].insert(16, "Mon State of Charge (%)", np.NaN)
        HouseData3[x].insert(24, "Tue State of Charge (%)", np.NaN)
        HouseData3[x].insert(32, "Wed State of Charge (%)", np.NaN)
        HouseData3[x].insert(40, "Thurs State of Charge (%)", np.NaN)
        HouseData3[x].insert(48, "Fri State of Charge (%)", np.NaN)
        HouseData3[x].insert(56, "Sat State of Charge (%)", np.NaN)
        HouseData3[x].insert(64, "Sun State of Charge (%)", np.NaN)

    #Adding extra weeks (however many we wish to run the simulation for)
    HouseData4 = {}
    for car in car_list:
        HouseData4[car] = pd.concat([HouseData3[car].iloc[:,9:]] * (weeks), axis=1, ignore_index=True)
        HouseData4[car].insert(0, 'Time', HouseData3[car].iloc[:,0]) #Adding the time column
        #Add Day 0 back in
        HouseData4[car].insert(1, "Day 0 Location", HouseData3[car]['Mon Location'])
        HouseData4[car].insert(2, "Day 0 Location Code", HouseData3[car]['Mon Location Code'])
        HouseData4[car].insert(3, "Day 0 Miles", HouseData3[car]['Mon Miles'])
        HouseData4[car].insert(4, "Day 0 Energy", HouseData3[car]['Mon Energy'])
        HouseData4[car].insert(5, "Day 0 Battery Capacity", np.NaN)
        HouseData4[car].insert(6, "Day 0 Charging Energy", np.NaN)
        HouseData4[car].insert(7, "Day 0 Charging Power", np.NaN)
        HouseData4[car].insert(8, "Day 0 State of Charge (%)", np.NaN)

        #reneame all the headings
        #needs to be done in a way which relates back to the variable 'weeks', so that its dynamic!!
        week_codes = list(range(1,weeks+1))
        days_of_week = ['Mon', 'Tue', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
        base_headings = ['Location', 'Location Code', 'Miles', 'Energy', 'Battery Capacity', 'Charging Energy', 'Charging Power', 'State of Charge (%)']

        final_headings = []

        for week in week_codes:
            for day in days_of_week:
                for base in base_headings:
                    p = day + str(week) + ' ' + base
                    final_headings.append(p)

        static_headings = ['Time', 'Day 0 Location', 'Day 0 Location Code', 'Day 0 Miles', 'Day 0 Energy', 'Day 0 Battery Capacity', 'Day 0 Charging Energy', 'Day 0 Charging Power', 'Day 0 State of Charge (%)']
        final_headings = static_headings + final_headings
        old = list(HouseData4[car])
        HouseData4[car].rename(columns={old[idx]: name for (idx, name) in enumerate(final_headings)}, inplace=True)




















    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------


















    #Now the dataframe is completed and ready for the actual charging and calculations to be done!!!!!
    #calculating leave and return times for each day for each car

    #for loop to make the dictionaries for each day
    week_day_numbers = []
    for week in week_codes:
        for day in days_of_week:
            p = day + str(week)
            week_day_numbers.append(p)
    week_day_numbers.insert(0, 'Day 0')



    LeaveTimes = {}
    LeaveTimeIndexs = {}
    HomeTimes = {}
    HomeTimeIndexs = {}

    for day in week_day_numbers:
        LeaveTimes[day] = {}
        LeaveTimeIndexs[day] = {}
        HomeTimes[day] = {}
        HomeTimeIndexs[day] = {}

    #making the column headings needed - need to make these for whatever the number of weeks there are
    loc_code = []
    loc_days = []
    for day in week_day_numbers:
        new = day + ' Location Code'
        loc_code.append(new)

    for day in week_day_numbers:
        new = day + ' Location'
        loc_days.append(new)

    for day, loccode, loc in zip(week_day_numbers, loc_code, loc_days):
        for x in car_list:
            for i in range(0, 47):
                if HouseData4[x][loccode][i] == 0:
                    #print("car is at home")
                    if HouseData4[x][loc][i] == HouseData4[x][loc][i+1]:
                        Time = {x:'Car Does Not Leave Home'}
                        LeaveTimes[day].update(Time)
                        Index = {x:'N/A'}
                        LeaveTimeIndexs[day].update(Index)
                    elif HouseData4[x][loc][i] != HouseData4[x][loc][i+1]:
                        Time = {x:HouseData4[x]["Time"][i+1]}
                        LeaveTimes[day].update(Time)
                        Index = {x:i+1}
                        LeaveTimeIndexs[day].update(Index)
                else: #This is the code for if the car (at midnight) is not at home (i.e. night shift worker)
                    break #only house 27 has this - do that house by hand

    #print('These are the LEAVE TIMES')
    #print(LeaveTimes)

    for day, loccode, loc in zip(week_day_numbers, loc_code, loc_days):
        for x in car_list:
            for i in range(47, 0, -1):
                #print(HouseData4[x][loccode][i])
                if HouseData4[x][loccode][i] == 0:
                    if HouseData4[x][loc][i] == HouseData4[x][loc][i-1]:
                        Time = {x:'Car Does Not Leave Home'}
                        HomeTimes[day].update(Time)
                        Index = {x:'N/A'}
                        HomeTimeIndexs[day].update(Index)
                    elif HouseData4[x][loc][i] != HouseData4[x][loc][i-1]:
                        Time = {x:HouseData4[x]["Time"][i]}
                        HomeTimes[day].update(Time)
                        Index = {x:i}
                        HomeTimeIndexs[day].update(Index)
                else: #This is the code for if the car (at midnight) is not at home (i.e. night shift worker)
                    break #only house 27 has this - do that house by hand

    #print('These are the HOME TIMES')
    #print(HomeTimes)





















    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------
















    #The whole next bit only goes ahead if its NOT house 27. House 27 blows up the code
    #so will have to do that one separately. The spreadsheets with all the necessary columns
    #will still be made from the code above, it just wont be filled in. Do this by hand afterwards!!
    if house == 'House 27':
        newpath = r'C:\Users\mckin\Desktop\Results - 8 Weeks'
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        for car in car_list:
            HouseData4[car].to_csv(r'C:\Users\mckin\Desktop\Results - 8 Weeks\ '+str(house)+' - '+str(car)+'.csv')
            #print(house,' - ',car, 'SAVED')
            #print('---------------------------------------------------------------------')
        continue
    else:
        #For all other houses run the calculation loops for charging etc!
        #Now to do the actual calulations for each day
        #DO DAY 0 SEPARATE! NOT IN LOOP WITH THE OTHER DAYS OF THE WEEK
        #DAY 0
        for x in car_list:
            HouseData4[x]['Day 0 Battery Capacity'] = SoC100 - HouseData4[x]['Day 0 Energy']
            if HomeTimeIndexs['Day 0'][x] != 'N/A':
                if HouseData4[x]["Day 0 Battery Capacity"][HomeTimeIndexs['Day 0'][x]] <= SoC20:
                    if ElecTariff>0 and ElecTariff<20: #i.e. Economy 7
                        HouseData4[x]["Mon1 Charging Energy"][0] = 0
                        HouseData4[x]["Mon1 Charging Energy"][1] = 3.3
                        HouseData4[x]['Mon1 Battery Capacity'][0] = HouseData4[x]['Day 0 Battery Capacity'][47]
                        HouseData4[x]['Mon1 Battery Capacity'][1] = HouseData4[x]['Day 0 Battery Capacity'][47] + HouseData4[x]["Mon1 Charging Energy"][1]
                        HouseData4[x]["Day 0 Charging Energy"][HomeTimeIndexs['Day 0'][x]:48] = 0
                    elif ElecTariff>20: #i.e. Standard
                        HouseData4[x]["Day 0 Charging Energy"][HomeTimeIndexs['Day 0'][x]+1:48] = 3.3
                        HouseData4[x]["Day 0 Charging Energy"][LeaveTimeIndexs['Day 0'][x]:HomeTimeIndexs['Day 0'][x]+1] = 0
                        HouseData4[x]["Day 0 Battery Capacity"][LeaveTimeIndexs['Day 0'][x]+1] = HouseData4[x]["Day 0 Battery Capacity"][LeaveTimeIndexs['Day 0'][x]+1] + HouseData4[x]["Day 0 Charging Energy"][LeaveTimeIndexs['Day 0'][x]+1]
                        for y in range(HomeTimeIndexs['Day 0'][x]+1, 49):
                            if HouseData4[x]["Day 0 Battery Capacity"][y-1] < SoC80:
                                HouseData4[x]["Day 0 Charging Energy"][y] = 3.3
                                HouseData4[x]["Day 0 Battery Capacity"][y] = HouseData4[x]["Day 0 Battery Capacity"][y-1] + HouseData4[x]["Day 0 Charging Energy"][y]
                            elif HouseData4[x]["Day 0 Battery Capacity"][y-1] >= SoC80:
                                delta = HouseData4[x]["Day 0 Battery Capacity"][y-1] - SoC80
                                HouseData4[x]["Day 0 Battery Capacity"][y-1] = HouseData4[x]["Day 0 Battery Capacity"][y-1] - delta
                                HouseData4[x]["Day 0 Charging Energy"][y-1] = HouseData4[x]["Day 0 Charging Energy"][y-1] - delta
                                HouseData4[x]["Day 0 Battery Capacity"][y] = HouseData4[x]["Day 0 Battery Capacity"][y-1]
                                HouseData4[x]["Day 0 Charging Energy"][y] = 0
                        HouseData4[x]["Mon1 Battery Capacity"][0] = HouseData4[x]["Day 0 Battery Capacity"][47]
                else:
                    h = HouseData4[x]["Day 0 Battery Capacity"][47]
                    HouseData4[x]["Mon1 Battery Capacity"][0] = h
                    HouseData4[x]["Mon1 Battery Capacity"][1] = h
                    HouseData4[x]["Day 0 Charging Energy"] = 0
                    HouseData4[x]["Mon1 Charging Energy"][0] = 0
                    HouseData4[x]["Mon1 Charging Energy"][1] = 0

            else: #i.e. the car is at home all day (so it says 'same' all the way through 'Day 0 Charging Energy')
                if HouseData4[x]["Day 0 Battery Capacity"][0] <= SoC20: #i.e. the car starts off with less than 20% (it cant as we are starting with 100%)
                    break #impossible scenario so dont need to bother charging
                else:
                    HouseData4[x]["Day 0 Charging Energy"] = 0 #puts zeros in this column (instead of the word 'same')
                    HouseData4[x]["Mon1 Battery Capacity"][0] = HouseData4[x]["Day 0 Battery Capacity"][47]
                    HouseData4[x]["Mon1 Battery Capacity"][1] = HouseData4[x]["Day 0 Battery Capacity"][47]
                    HouseData4[x]["Mon1 Charging Energy"][0] = 0
                    HouseData4[x]["Mon1 Charging Energy"][1] = 0


        #MONDAY TO SUNDAY LOOP FOR HOWEVER MANY WEEKS THE SIMULATION RUNS
        for x in car_list:
            for index, daynum in enumerate(week_day_numbers):
                if daynum == 'Day 0':
                    continue
                else:
                    #print('Calculating', daynum, 'for', x)
                    if ElecTariff<20: #i.e. Economy 7
                        #CHECK IF ITS CHARGING GOING INTO MONDAY
                        #if the second charging row is zero then its deffo not going into that day charging or starting charging at midngiht
                        if HouseData4[x][daynum + " Charging Energy"][1] == 0:
                            HouseData4[x][daynum + " Battery Capacity"] = HouseData4[x][week_day_numbers[index-1] + " Battery Capacity"][47] - HouseData4[x][daynum + " Energy"]
                        else:
                            continue
                    else:
                        HouseData4[x][daynum + " Battery Capacity"] = HouseData4[x][daynum + " Battery Capacity"][0] - HouseData4[x][daynum + " Energy"]
                    if ElecTariff>20:
                        #if standard meter
                        if LeaveTimeIndexs[daynum][x] != 'N/A':
                            for i in range(0, 48):
                                if HouseData4[x][daynum + " Charging Energy"][i] == 3.3: #marker of
                                    HouseData4[x][daynum + " Battery Capacity"][i] = HouseData4[x][daynum + " Battery Capacity"][i] + 3.3
                                    if HouseData4[x][daynum + " Battery Capacity"][i] < SoC80 and i < LeaveTimeIndexs[daynum][x]: #fully charged stops or leaves home
                                        HouseData4[x][daynum + " Charging Energy"][i+1] = 3.3
                                        HouseData4[x][daynum + " Battery Capacity"][i+1] = HouseData4[x][daynum + " Battery Capacity"][i]
                                    else:
                                        if HouseData4[x][daynum + " Battery Capacity"][i] >= SoC80:
                                            delta = HouseData4[x][daynum + " Battery Capacity"][i] - SoC80
                                            HouseData4[x][daynum + " Charging Energy"][i] = HouseData4[x][daynum + " Charging Energy"][i] - delta
                                            HouseData4[x][daynum + " Battery Capacity"][i] = HouseData4[x][daynum + " Battery Capacity"][i] - delta
                                            HouseData4[x][daynum + " Charging Energy"][i+1] = 0
                                            HouseData4[x][daynum + " Battery Capacity"][i+1] = 29.6
                                            if i > LeaveTimeIndexs[daynum][x]:
                                                break
                                else:
                                    HouseData4[x][daynum + " Charging Energy"][i] = 0
                                    if i != 0:
                                        HouseData4[x][daynum + " Battery Capacity"][i] = HouseData4[x][daynum + " Battery Capacity"][i-1]
                        else:
                            for i in range(0, 48):
                                if HouseData4[x][daynum + " Charging Energy"][i] == 3.3:
                                    HouseData4[x][daynum + " Battery Capacity"][i] = HouseData4[x][daynum + " Battery Capacity"][i] + 3.3
                                    if HouseData4[x][daynum + " Battery Capacity"][i] < SoC80:
                                        HouseData4[x][daynum + " Charging Energy"][i+1] = 3.3
                                        HouseData4[x][daynum + " Battery Capacity"][i+1] = HouseData4[x][daynum + " Battery Capacity"][i] + 3.3
                                    else:
                                        if HouseData4[x][daynum + " Battery Capacity"][i] >= SoC80:
                                            delta = HouseData4[x][daynum + " Battery Capacity"][i] - SoC80
                                            HouseData4[x][daynum + " Charging Energy"][i] = HouseData4[x][daynum + " Charging Energy"][i] - delta
                                            HouseData4[x][daynum + " Battery Capacity"][i] = HouseData4[x][daynum + " Battery Capacity"][i] - delta
                                            if LeaveTimeIndexs[daynum][x] != 'N/A':
                                                if i > LeaveTimeIndexs[daynum][x]:
                                                    break
                                else:
                                    HouseData4[x][daynum + " Charging Energy"][i] = 0
                                    if daynum != week_day_numbers[-1]:
                                        HouseData4[x][week_day_numbers[index+1] + " Battery Capacity"][0] = HouseData4[x][daynum + " Battery Capacity"][47]
                                        HouseData4[x][week_day_numbers[index+1] + " Battery Capacity"][1] = HouseData4[x][daynum + " Battery Capacity"][47]
                                        HouseData4[x][week_day_numbers[index+1] + " Charging Energy"][0] = 0
                                        HouseData4[x][week_day_numbers[index+1] + " Charging Energy"][1] = 0

                    else: #economy meter
                        if LeaveTimeIndexs[daynum][x] != 'N/A':
                            for i in range(1,LeaveTimeIndexs[daynum][x]+2):
                                if HouseData4[x][daynum + " Charging Energy"][i] == 3.3: #then its charging going into the day
                                    if HouseData4[x][daynum + " Battery Capacity"][i] < SoC80:
                                        HouseData4[x][daynum + " Charging Energy"][i+1] = 3.3
                                        HouseData4[x][daynum + " Battery Capacity"][i+1] = HouseData4[x][daynum + " Battery Capacity"][i] + 3.3
                                    elif HouseData4[x][daynum + " Battery Capacity"][i-1] < SoC80 and HouseData4[x][daynum + " Battery Capacity"][i] >= SoC80:
                                        delta = HouseData4[x][daynum + " Battery Capacity"][i] - SoC80
                                        HouseData4[x][daynum + " Charging Energy"][i] = HouseData4[x][daynum + " Charging Energy"][i] - delta
                                        HouseData4[x][daynum + " Battery Capacity"][i] = HouseData4[x][daynum + " Battery Capacity"][i] - delta
                                        HouseData4[x][daynum + " Charging Energy"][i+1] = 0
                                        HouseData4[x][daynum + " Battery Capacity"][i+1] = SoC80
                                    elif HouseData4[x][daynum + " Battery Capacity"][i] == SoC80:
                                        HouseData4[x][daynum + " Charging Energy"][i] = 0
                                        HouseData4[x][daynum + " Battery Capacity"][i] = SoC80
                                else:
                                    if HouseData4[x][daynum + " Charging Energy"][i] == 0:
                                        HouseData4[x][daynum + " Charging Energy"][i+1] = 0
                                        HouseData4[x][daynum + " Battery Capacity"][i] = HouseData4[x][daynum + " Battery Capacity"][i-1]
                        else:
                            if HouseData4[x][daynum + " Charging Energy"][1] == 3.3:
                                for i in range(1,48):
                                    if HouseData4[x][daynum + " Battery Capacity"][i] < SoC80:
                                        HouseData4[x][daynum + " Charging Energy"][i+1] = 3.3
                                        HouseData4[x][daynum + " Battery Capacity"][i+1] = HouseData4[x][daynum + " Battery Capacity"][i] + 3.3
                                    elif HouseData4[x][daynum + " Battery Capacity"][i-1] < SoC80 and HouseData4[x][daynum + " Battery Capacity"][i] > SoC80:
                                        delta = HouseData4[x][daynum + " Battery Capacity"][i] - SoC80
                                        HouseData4[x][daynum + " Charging Energy"][i] = HouseData4[x][daynum + " Charging Energy"][i] - delta
                                        HouseData4[x][daynum + " Battery Capacity"][i] = HouseData4[x][daynum + " Battery Capacity"][i] - delta
                                        HouseData4[x][daynum + " Charging Energy"][i+1] = 0
                                        HouseData4[x][daynum + " Battery Capacity"][i+1] = SoC80
                                    elif HouseData4[x][daynum + " Battery Capacity"][i] == SoC80:
                                        HouseData4[x][daynum + " Charging Energy"][i+1] = 0
                                        HouseData4[x][daynum + " Battery Capacity"][i+1] = SoC80
                                        if daynum != week_day_numbers[-1]:
                                            HouseData4[x][week_day_numbers[index+1] + " Battery Capacity"][0] = HouseData4[x][daynum + " Battery Capacity"][47]
                                            HouseData4[x][week_day_numbers[index+1] + " Battery Capacity"][1] = HouseData4[x][daynum + " Battery Capacity"][47]
                                            HouseData4[x][week_day_numbers[index+1] + " Charging Energy"][0] = 0
                                            HouseData4[x][week_day_numbers[index+1] + " Charging Energy"][1] = 0
                            else:
                                for i in range(1,48):
                                    HouseData4[x][daynum + " Charging Energy"][i] = 0
                                if daynum != week_day_numbers[-1]:
                                    HouseData4[x][week_day_numbers[index+1] + " Battery Capacity"][0] = HouseData4[x][daynum + " Battery Capacity"][47]
                                    HouseData4[x][week_day_numbers[index+1] + " Battery Capacity"][1] = HouseData4[x][daynum + " Battery Capacity"][47]
                                    HouseData4[x][week_day_numbers[index+1] + " Charging Energy"][0] = 0
                                    HouseData4[x][week_day_numbers[index+1] + " Charging Energy"][1] = 0
                    if LeaveTimeIndexs[daynum][x] != 'N/A':
                        #print(HomeTimeIndexs[daynum][x])
                        for i in range(LeaveTimeIndexs[daynum][x],HomeTimeIndexs[daynum][x]+1):
                            HouseData4[x][daynum + " Charging Energy"][i] = 0
                            HouseData4[x][daynum + " Battery Capacity"][i] = HouseData4[x][daynum + " Battery Capacity"][LeaveTimeIndexs[daynum][x]] - HouseData4[x][daynum + " Energy"][i]
                    else:
                        continue
                    if LeaveTimeIndexs[daynum][x] != 'N/A':
                        if HouseData4[x][daynum + " Battery Capacity"][HomeTimeIndexs[daynum][x]] <= SoC20:
                            if ElecTariff>0 and ElecTariff<20: #i.e. Economy 7
                                HouseData4[x][daynum + " Charging Energy"][HomeTimeIndexs[daynum][x]:48] = 0
                                HouseData4[x][daynum + " Battery Capacity"][HomeTimeIndexs[daynum][x]:48] = HouseData4[x][daynum + " Battery Capacity"][HomeTimeIndexs[daynum][x]]
                                if daynum != week_day_numbers[-1]:
                                    HouseData4[x][week_day_numbers[index+1] + " Charging Energy"][0] = 0
                                    HouseData4[x][week_day_numbers[index+1] + " Charging Energy"][1] = 3.3
                                    HouseData4[x][week_day_numbers[index+1] + " Battery Capacity"][0] = HouseData4[x][daynum + " Battery Capacity"][47]
                                    HouseData4[x][week_day_numbers[index+1] + " Battery Capacity"][1] = HouseData4[x][daynum + " Battery Capacity"][47] + HouseData4[x][week_day_numbers[index+1] + " Charging Energy"][1]
                                else:
                                    continue
                            elif ElecTariff>20: #i.e. Standard
                                HouseData4[x][daynum + " Charging Energy"][HomeTimeIndexs[daynum][x]+1:48] = 3.3
                                HouseData4[x][daynum + " Charging Energy"][LeaveTimeIndexs[daynum][x]:HomeTimeIndexs[daynum][x]+1] = 0
                                HouseData4[x][daynum + " Battery Capacity"][LeaveTimeIndexs[daynum][x]+1] = HouseData4[x][daynum + " Battery Capacity"][LeaveTimeIndexs[daynum][x]+1] + HouseData4[x][daynum + " Charging Energy"][LeaveTimeIndexs[daynum][x]+1]
                                for y in range(HomeTimeIndexs[daynum][x]+1, 49):
                                    if HouseData4[x][daynum + " Battery Capacity"][y-1] < SoC80:
                                        HouseData4[x][daynum + " Charging Energy"][y] = 3.3
                                        HouseData4[x][daynum + " Battery Capacity"][y] = HouseData4[x][daynum + " Battery Capacity"][y-1] + HouseData4[x][daynum + " Charging Energy"][y]
                                        #HouseData4[x][week_day_numbers[index+1] + " Charging Energy"][0] = 3.3
                                        #HouseData4[x][week_day_numbers[index+1] + " Charging Energy"][1] = 3.3
                                        #HouseData4[x][week_day_numbers[index+1] + " Battery Capacity"][0] = HouseData4[x][daynum + " Battery Capacity"][47] + 3.3
                                        #HouseData4[x][week_day_numbers[index+1] + " Battery Capacity"][1] = HouseData4[x][daynum + " Battery Capacity"][47] + 6.6
                                    elif HouseData4[x][daynum + " Battery Capacity"][y-1] >= SoC80:
                                        delta = HouseData4[x][daynum + " Battery Capacity"][y-1] - SoC80
                                        HouseData4[x][daynum + " Battery Capacity"][y-1] = HouseData4[x][daynum + " Battery Capacity"][y-1] - delta
                                        HouseData4[x][daynum + " Charging Energy"][y-1] = HouseData4[x][daynum + " Charging Energy"][y-1] - delta
                                        HouseData4[x][daynum + " Battery Capacity"][y] = HouseData4[x][daynum + " Battery Capacity"][y-1]
                                        HouseData4[x][daynum + " Charging Energy"][y] = 0
                                #if HouseData4[x][daynum + " Battery Capacity"][48] < SoC80: #THIS LINE SOLVES THE PROBLEM
                                if daynum != week_day_numbers[-1]:
                                    print('HERE CHECK 1')
                                    HouseData4[x][week_day_numbers[index+1] + " Battery Capacity"][0] = HouseData4[x][daynum + " Battery Capacity"][47]
                                    if HouseData4[x][daynum + " Battery Capacity"][48] < SoC80:
                                        HouseData4[x][week_day_numbers[index+1] + " Battery Capacity"][0] = HouseData4[x][daynum + " Battery Capacity"][47]
                                        HouseData4[x][week_day_numbers[index+1] + " Charging Energy"][0] = 3.3
                                        #HouseData4[x][week_day_numbers[index+1] + " Battery Capacity"][1] = HouseData4[x][daynum + " Battery Capacity"][47] + 6.6
                                        #HouseData4[x][week_day_numbers[index+1] + " Charging Energy"][1] = 3.3
                                else:
                                    continue
                        else:
                            for i in range(HomeTimeIndexs[daynum][x], 48):
                                HouseData4[x][daynum + " Charging Energy"][i] = 0
                                HouseData4[x][daynum + " Battery Capacity"][i] = HouseData4[x][daynum + " Battery Capacity"][HomeTimeIndexs[daynum][x]]
                            if daynum != week_day_numbers[-1]:
                                HouseData4[x][week_day_numbers[index+1] + " Battery Capacity"][0] = HouseData4[x][daynum + " Battery Capacity"][47]
                                HouseData4[x][week_day_numbers[index+1] + " Battery Capacity"][1] = HouseData4[x][daynum + " Battery Capacity"][47]
                                HouseData4[x][week_day_numbers[index+1] + " Charging Energy"][0] = 0
                                HouseData4[x][week_day_numbers[index+1] + " Charging Energy"][1] = 0
                            else:
                                continue
                    else:
                        print('HERE CHECK 2')
                        #HouseData4[x][daynum + " Charging Energy"] = 0
                        if daynum != week_day_numbers[-1]:
                            HouseData4[x][week_day_numbers[index+1] + " Battery Capacity"][0] = HouseData4[x][daynum + " Battery Capacity"][47]
                            HouseData4[x][week_day_numbers[index+1] + " Battery Capacity"][1] = HouseData4[x][daynum + " Battery Capacity"][47]
                            HouseData4[x][week_day_numbers[index+1] + " Charging Energy"][0] = 0
                            HouseData4[x][week_day_numbers[index+1] + " Charging Energy"][1] = 0
                        else:
                            continue
                        HouseData4[x][daynum + " Charging Energy"] = 0

        #'Charging Power' & 'State of Charge' column calculations loop
        for x in car_list:
            for index, daynum in enumerate(week_day_numbers):
                for i in range(0, 48):
                    if HouseData4[x][daynum + " Charging Energy"][i] != 0:
                        HouseData4[x][daynum + " Charging Power"][i] = 6.6
                    else:
                        HouseData4[x][daynum + " Charging Power"][i] = 0
                    HouseData4[x][daynum + " State of Charge (%)"][i] = (HouseData4[x][daynum + " Battery Capacity"][i]/37)*100


    #dynamic filesaving name and saving all results to a new folder on the desktop
    newpath = r'C:\Users\mckin\Desktop\(80-20%) -100% Stand'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    for car in car_list:
        HouseData4[car].to_csv(r'C:\Users\mckin\Desktop\(80-20%) -100% Stand\ '+str(house)+' - '+str(car)+'.csv')

    print(house,' - ',car, 'SAVED')
    print('---------------------------------------------------------------------')

#print(week_day_numbers)
