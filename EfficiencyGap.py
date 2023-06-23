#Efficiency gap calculatiions with 2021 data
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('Georgia_Voting_Data.csv')

num_districts = len(data.index)
data["VOTES TO WIN"] = data["TOTAL VOTES"]/2
data["WASTED DEM VOTES"] = 0 
data["WASTED REP VOTES"] = 0

for i in range(num_districts):
  if data["DEM VOTES"][i] > data["REP VOTES"][i]: #if the nmbr of dem votes is greater than rep votes at step i
    data.loc[i,"WASTED REP VOTES"] = data.loc[i,"REP VOTES"]#locate & access to postion i and initialize wasted votes in that district
    data.loc[i,"WASTED DEM VOTES"] = data.loc[i,"DEM VOTES"] - data.loc[i,"VOTES TO WIN"]
  if data["REP VOTES"][i] > data["DEM VOTES"][i]:
    data.loc[i,"WASTED DEM VOTES"] = data.loc[i,"DEM VOTES"]
    data.loc[i,"WASTED REP VOTES"] = data.loc[i,"REP VOTES"] - data.loc[i,"VOTES TO WIN"]

data["EFFICIENCY GAP"] = 0
for i in range(num_districts):#find net wasted votes for each district (wasted dem- wasted rep)/total
  if data.loc[i,'WASTED DEM VOTES'] > data.loc[i,'WASTED REP VOTES']:#make sure that the number i get won't be negative
    data.loc[i, "EFFICIENCY GAP"] = 100 * (data.loc[i,'WASTED DEM VOTES'] - data.loc[i,'WASTED REP VOTES']) / (data.loc[i, 'TOTAL VOTES'])
  else:
    data.loc[i, "EFFICIENCY GAP"] = 100 * (data.loc[i,'WASTED REP VOTES'] - data.loc[i,'WASTED DEM VOTES']) / (data.loc[i, 'TOTAL VOTES'])

data.loc[len(data)] = 0
for i in range(num_districts):
  data.loc[num_districts, 'TOTAL VOTES'] += data.loc[i, 'TOTAL VOTES']
  data.loc[num_districts, 'WASTED DEM VOTES'] += data.loc[i, 'WASTED DEM VOTES']
  data.loc[num_districts, 'WASTED REP VOTES'] += data.loc[i, 'WASTED REP VOTES']
data.loc[num_districts, 'EFFICIENCY GAP'] = 100 * (data.loc[num_districts, 'WASTED DEM VOTES'] - data.loc[num_districts, 'WASTED REP VOTES']) / data.loc[num_districts, 'TOTAL VOTES']

print(data)
