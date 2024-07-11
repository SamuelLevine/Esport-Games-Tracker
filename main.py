import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
from tkinter import N
import csv
import numpy as np

driver = webdriver.Chrome()
url = "https://www.strafe.com/calendar/lol/"
driver.get(url)
data = []

# Automatically scroll the page
scroll_pause_time = 1  # Pause between each scroll
screen_height = driver.execute_script("return window.screen.height;")  # Browser window height
i = 1
while True:
    # Scroll down
    driver.execute_script(f"window.scrollTo(0, {screen_height * i});")
    i += 1
    time.sleep(scroll_pause_time)

    # Check if reaching the end of the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    if screen_height * i > scroll_height:
        break

#Turn fully scrolled through webpage into soup to parse through. 
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()
    
#Blocked out each day of matches
all_daysofmatches = soup.find_all("div", class_="calendar_section__wwKUT")

#Scrape through each all_daysofmatches block and return the date and teams playing
for event in all_daysofmatches:
    
    #Find the date in each all_daysofmatches block and print it
    for tag in event.find("h2", class_="calendar_sectionHeader__um_sQ m-0 p-0 text-base capitalize"):
        data.append(tag.text)

    #Find all teams playing (in order) on the current date
    for tag in event.find_all("span", itemprop="competitor"):
        data.append(tag.text)

#Find all links with this itemtype, resulting in all match links
links = soup.find_all("a", itemtype="https://schema.org/SportsEvent")
for link in links:
    newlink = "https://www.strafe.com" + link.get("href")
    data.append(newlink)

#Input the data into a data frame and send it to a csv
df = pd.DataFrame(data)
df.to_csv("matches.csv")

# Inital testing to get match links and find teams by parsing the new links
"""
currentday = {}
currentday['Link'] = event.find("a", itemtype="https://schema.org/SportsEvent", class_="calendar_match__OVPtl").attrs["href"]
newurl = "https://www.strafe.com" + currentday['Link']
print(newurl)


individualmatches = soup.find_all("a", itemtype="https://schema.org/SportsEvent", class_="calendar_match_OVPtl")    #Holds all info for each match on a day

for game in individualmatches:
    currentteam = {}
    currentteam['Team'] = event.find("span", itemprop="competitor").text
    print(currentteam['Team'])

for matches in currentdayofmatches:
    currentmatch = {}
    currentmatch['Teams'] = event.find("img").attrs["alt"]
    print(currentmatch['Teams'])
"""

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
    if "202" in matchesSeries[i]:
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
        #Make the date column empty if match is on the same day as previous match
        dates_array[dates_index] = ' '
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
#df.to_csv("organizedmatches.csv")
df.to_html("matchtable.html", index = False)