# File: metar.py
# Author: Hayden Sapp
# Date: 2022-05-11
#
# Function:
#   This program takes METAR data and decodes it into a human readable format
#
#Imports---------------------------------------------------------------
import requests #Web Scraping
from bs4 import BeautifulSoup #Web Scraping
from datetime import datetime #Current Date
import os #Clear Terminal
#-----------------------------------------------------------------------
#               Functions
#-----------------------------------------------------------------------
#Converts month as a number to a string
def monthToStr(month):
    monthList = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    return monthList[month-1]
#Converts ZULU to MST
def zToMst(z):
    time = 0
    if (z < 7):
        time = 24-7+z
    else:
        time = z-7
    return time
#converts a degrees to a direction
def degreesToDir(deg):
    dir = ""
    if deg > 0 and deg <= 45:
        dir = "North North East"
    elif deg > 45 and deg < 90:
        dir = "North East"
    elif deg > 90 and deg <= 135:
        dir = "South East"
    elif deg > 135 and deg < 180:
        dir = "South South East"
    elif deg > 180 and deg <= 225:
        dir = "South South West"
    elif deg > 225 and deg < 270:
        dir = "South West"
    elif deg > 270 and deg <= 315:
        dir = "North West"
    elif deg > 315 and deg < 360:
        dir = "North North West"
    elif deg == 90:
        dir = "East"
    elif deg == 180:
        dir = "South"
    elif deg == 270:
        dir = "West"
    elif deg == 0 or deg == 360:
        dir = "North"
    return dir
def main():
    #Clear the terminal
    os.system("cls")
    #Ask which station METAR to get data from
    stationID = str(input("What station ID do you want a METAR data of? "))
    #Join the station ID with the URL
    url = "https://www.aviationweather.gov/metar/data?ids=" + stationID.upper() + "&format=raw&date=&hours=0"
    page = requests.get(url)
    #parse the HTML document
    soup = BeautifulSoup(page.content, "html.parser")
    #The data is in a <code> tag in the website, so search for that tag
    report = soup.findAll('code')
    for data in report:
        print("\n\n-------- Whole Report --------\n")
        print(data.text)
        dataArray = data.text
    #Split the whole report into different sections
    dataArray = list(dataArray.split(" "))
    #Station -----------------------------------------------------------------------
    print("\n-------- Station --------\n")
    print("Station ID: " + dataArray[0])
    #date -----------------------------------------------------------------------
    print("\n-------- Date --------\n")
    date = dataArray[1]
    date = list(date)
    #Get the current month
    month = datetime.now().month
    #convert to string
    month = monthToStr(month)
    print("Date: " + date[0] + date[1] + "th of " + month)
    #time -----------------------------------------------------------------------
    print("\n-------- Time --------\n")
    print("Time (Zulu): " + date[2] + date[3] + ":" + date[4] + date[5])
    zulu = date[2]+date[3]
    #convert z to mst
    mstTime = zToMst(int(zulu))
    print("Time (MST): " + str(mstTime) + ":" + date[4] + date[5])
    #wind -----------------------------------------------------------------------
    print("\n-------- Wind --------\n")
    wind = dataArray[2]
    wind = list(wind)
    windDeg = wind[0] + wind[1] + wind[2]
    windDir = degreesToDir(int(windDeg))
    print("Wind Direction: " + windDeg + " degrees. It is coming from the " + windDir)
    print("Wind Speed: " + wind[3] + wind[4] + " Knots")
    #If there is a G in the report, there are significant gusts
    if "G".upper() in wind:
        print("Wind Gusts: " + wind[6] + wind[7] + " Knots")
    #visibility -----------------------------------------------------------------------
    print("\n-------- Visibility --------\n")
    vis = dataArray[3]
    vis = list(vis)
    print("Visibility: " + vis[0] + vis[1] + " Statute Miles")
    #Cloud Cover -----------------------------------------------------------------------
    print("\n-------- Cloud Cover --------\n")
    cc = dataArray[4]
    coverTypes = ["CLR", "FEW", "SCT", "BKN", "OVC", "TCU"]
    coverNames = ["Clear", "Few Clouds", "Scattered Clouds", "Broken Clouds", "Overcast", "Towering Cumulus Cloud"]
    height = cc[3]+cc[4]+cc[5]
    index = 0
    tempIndex=5
    for type in coverTypes:
        if type in cc:
            print("There is " + coverNames[index] + " reported at ", end="")
        index+=1
    cc = list(cc)
    print(height + "00 feet AGL")
    cc2 = dataArray[5]
    for type in coverTypes:
        if type in cc2:
            height2 = cc2[3]+cc2[4]+cc2[5]
            index = 0
            for type in coverTypes:
                if type in cc2:
                    print("There is " + coverNames[index] + " reported at ", end="")
                index+=1
            cc2 = list(cc2)
            print(height2 + "00 feet AGL")
            tempIndex = 6
    cc3 = dataArray[6]
    for type in coverTypes:
        if type in cc3:
            height3 = cc3[3]+cc3[4]+cc3[5]
            index = 0
            for type in coverTypes:
                if type in cc3:
                    print("There is " + coverNames[index] + " reported at ", end="")
                index+=1
            cc3 = list(cc3)
            print(height3 + "00 feet AGL")
            tempIndex = 7
    #Temperature -----------------------------------------------------------------------
    print("\n-------- Temperature --------\n")
    temp = dataArray[tempIndex]
    temp = list(temp)
    if temp[0] == "M":
        temperature = temp[1]+temp[2]
        print("The temperature is -" + temperature + " degrees C", end="")
        if temp[4] == "M":
            dewPoint = temp[5]+temp[6]
            print(" and a Dew Point of -" + dewPoint + " degrees C")
        else:
            dewPoint = temp[4]+temp[5]
            print(" and a Dew Point of " + dewPoint + " degrees C")
    else:
        temperature = temp[0]+temp[1]
        print("The temperature is " + temperature + " degrees C", end="")
        if temp[3] == "M":
            dewPoint = temp[4]+temp[5]
            print(" and a Dew Point of -" + dewPoint + " degrees C")
        else:
            dewPoint = temp[3]+temp[4]
            print(" and a Dew Point of " + dewPoint + " degrees C")
    #Pressure -----------------------------------------------------------------------
    print("\n-------- Pressure --------\n")
    pressure = dataArray[tempIndex+1]
    pressure = list(pressure)
    print("The pressure is currently: " + pressure[1] + pressure[2] + "." + pressure[3] + pressure[4] + "\" Hg")
#-----------------------------------------------------------------------
#                               Main
#-----------------------------------------------------------------------
main()
