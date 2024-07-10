from tkinter import N
import pandas as pd
import csv
import numpy as np

#Turn the matches csv into a data fram
df = pd.read_csv("matches.csv")
#Turn the single column data frame into a series
matchesSeries = df.iloc[:,1]

#Create an array for each column of the new Data Frame
series_size = matchesSeries.size
dates_array = [0]*series_size
team1_array = [0]*series_size
team2_array = [0]*series_size
matchlink_array = [0]*series_size

#Go through each row of the csv and add each item to its appropriate array
sorted = False
i = 0
team1_index = 0
team2_index = 0
dates_index = 0
matchlink_index = 0
isFirstTeam = True
while sorted == False:
    #Check if we have reached the end of the csv/series passed in
    if "https" in matchesSeries[i]:
        break
    #Check if the row is a date, if so add it to the dates_array
    if "2024" in matchesSeries[i]:
        dates_array[dates_index] = matchesSeries[i]
        i += 1
        continue
    #If not a date or link, add first team to team1_array and second team to team2_array
    elif isFirstTeam == True:
        team1_array[team1_index] = matchesSeries[i]
        team1_index += 1
        isFirstTeam = False
        i += 1
        continue
    elif isFirstTeam == False:
        team2_array[team2_index] = matchesSeries[i]
        team2_index += 1
        isFirstTeam = True
        dates_index += 1
        i += 1
        continue

#Add the match links to matchlink_array
while True:
    if matchlink_index < len(matchlink_array):
        if i < series_size:
            matchlink_array[matchlink_index] = matchesSeries[i]
            matchlink_index += 1
            i += 1
        else:
            break
    else:
        break
        

#Turn the arrays into series using pandas
dates_series = pd.Series(dates_array)
team1_series = pd.Series(team1_array)
team2_series = pd.Series(team2_array)
matchlink_series = pd.Series(matchlink_array)

#Combine the series into a dataframe using pandas
df = pd.DataFrame({'Dates': dates_series, 'Team 1': team1_series, 'Team 2': team2_series, 'Match Links': matchlink_series})
#Cut any rows from the dataframe that have a '0' in the 'Team 1' column, meaning the rows is empty
df = df[df["Team 1"] != 0]
#Convert the dataframe to a csv
df.to_csv("organizedmatches.csv")