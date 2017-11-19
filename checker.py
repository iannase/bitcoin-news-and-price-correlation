# Ian Annase
# 11/18/17

import feedparser
import os
from datetime import datetime
import csv
import pytz
import xlsxwriter
from prettytable import PrettyTable
import time
from colorama import Fore, Back, Style
 
# function to fetch the rss feed and return the parsed rss
def parseRSS( rss_url ):
    return feedparser.parse( rss_url ) 

# parse the csv file into arrays
wordArray=[]
min5Array=[]
min10Array=[]
min15Array=[]
min20Array=[]
min25Array=[]
min30Array=[]
min35Array=[]
min40Array=[]
min45Array=[]
min50Array=[]
min55Array=[]
hour1Array=[]
hour2Array=[]
hour3Array=[]
hour4Array=[]
hour5Array=[]
hour6Array=[]
countArray=[]

# open CSV
with open('input.csv','r') as csv_file:
    csv_reader = csv.reader(csv_file)
    print()
    print("Loading...")
    print()
    z=0
    for line in csv_reader:
        if z == 0:
            z+=1
            continue

        wordArray.append(line[0])
        min5Array.append(line[1])
        min10Array.append(line[2])
        min15Array.append(line[3])
        min20Array.append(line[4])
        min25Array.append(line[5])
        min30Array.append(line[6])
        min35Array.append(line[7])
        min40Array.append(line[8])
        min45Array.append(line[9])
        min50Array.append(line[10])
        min55Array.append(line[11])
        hour1Array.append(line[12])
        hour2Array.append(line[13])
        hour3Array.append(line[14])
        hour4Array.append(line[15])
        hour5Array.append(line[16])
        hour6Array.append(line[17])
        countArray.append(line[18])

# welcome the user
print(">>> WELCOME <<<")
print("This application compares bitcoin price changes with the titles of news articles.")
print("It uses data gathered from past bitcoin prices down to the minute.")
print("There were 52,951 articles and 459,638 words analyzed between February 2015 and October 2017.")
print("The bitcoin price when the article came out was compared with the price at certain time intervals.")
print("The average price change for every word is being used as the dataset for this program.")

print("")

while True:
    print(">>> MAIN MENU <<<")
    print("1 - Launch the automatic RSS feed (see price predictions immediately when new articles come out)")
    print("2 - See the 15 most recent bitcoin articles with price predictions.")
    print("3 - Enter your own title/words to see what the price predictions are.")
    print("0 - Exit")
    print()
    choice = input("Enter your choice (0-3): ")
    print()

    # exit
    if choice == "0":
        break

    # first menu option
    if choice == "1":
        titles=[]
        z=0
        print("Scanning for new articles...")
        print()

        while True:
            # parse the RSS feed
            newsurl = ['http://www.bitnewz.net/rss/feed/15']
            feed = parseRSS( newsurl[0] )

            if z == 0:
                for newsitem in feed['items']: 
                    title=newsitem['title']
                    titles.append(title)
                z+=1
                continue
            else:
                for newsitem in feed['items']: 
                    title=newsitem['title']
                    date=newsitem['published']

                    if title not in titles:
                        os.system('say "new article detected"')
                        # convert the timezone to US eastern
                        fmt = "%m/%d/%Y %I:%M%p"
                        tz = 'US/Eastern'
                        d = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S Z')
                        awareTime = pytz.utc.localize(d)
                        easternTime = awareTime.astimezone(pytz.timezone(tz))
                        dateFormatted = easternTime.strftime(fmt)

                        # match the timestamp to the closest minute
                        timestamp = int(d.strftime("%s"))
                        mod=timestamp%60
                        timestamp=timestamp-mod

                        # make title only alphanumeric
                        titleLower=title.lower()
                        formattedTitle=""
                        validLetters = "abcdefghijklmnopqrstuvwxyz0123456789 "
                        for char in titleLower:
                            if char in validLetters:
                                formattedTitle+=char

                        # print title and date
                        print(title.upper())
                        print(dateFormatted)

                        # minute and hour charts headers
                        m = PrettyTable(['WORD', '5M', '10M', '15M', '20M', '25M', '30M', '35M', '40M', '45M', '50M', '55M', 'COUNT'])
                        mAvg = PrettyTable(['5M', '10M', '15M', '20M', '25M', '30M', '35M', '40M', '45M', '50M', '55M'])

                        words = formattedTitle.split()

                        # arrays of results to later take an average of
                        min5results=[]
                        min10results=[]
                        min15results=[]
                        min20results=[]
                        min25results=[]
                        min30results=[]
                        min35results=[]
                        min40results=[]
                        min45results=[]
                        min50results=[]
                        min55results=[]
                        countResults=[]

                        for x in words:
                            if x in wordArray:
                                index = wordArray.index(x)

                                min5result = min5Array[index]
                                min10result = min10Array[index]
                                min15result = min15Array[index]
                                min20result = min20Array[index]
                                min25result = min25Array[index]
                                min30result = min30Array[index]
                                min35result = min35Array[index]
                                min40result = min40Array[index]
                                min45result = min45Array[index]
                                min50result = min50Array[index]
                                min55result = min55Array[index]
                                countResult = countArray[index]

                                min5color=""
                                min10color=""
                                min15color=""
                                min20color=""
                                min25color=""
                                min30color=""
                                min35color=""
                                min40color=""
                                min45color=""
                                min50color=""
                                min55color=""

                                min5results.append(float(min5result[:-1]))
                                min10results.append(float(min10result[:-1]))
                                min15results.append(float(min15result[:-1]))
                                min20results.append(float(min20result[:-1]))
                                min25results.append(float(min25result[:-1]))
                                min30results.append(float(min30result[:-1]))
                                min35results.append(float(min35result[:-1]))
                                min40results.append(float(min40result[:-1]))
                                min45results.append(float(min45result[:-1]))
                                min50results.append(float(min50result[:-1]))
                                min55results.append(float(min55result[:-1]))
                                countResults.append(int(countResult))

                                if float(min5result[:-1]) > 0:
                                    min5color = Back.GREEN+min5result+Style.RESET_ALL
                                else:
                                    min5color = Back.RED+min5result+Style.RESET_ALL

                                if float(min10result[:-1]) > 0:
                                    min10color = Back.GREEN+min10result+Style.RESET_ALL
                                else:
                                    min10color = Back.RED+min10result+Style.RESET_ALL

                                if float(min15result[:-1]) > 0:
                                    min15color = Back.GREEN+min15result+Style.RESET_ALL
                                else:
                                    min15color = Back.RED+min15result+Style.RESET_ALL

                                if float(min20result[:-1]) > 0:
                                    min20color = Back.GREEN+min20result+Style.RESET_ALL
                                else:
                                    min20color = Back.RED+min20result+Style.RESET_ALL

                                if float(min25result[:-1]) > 0:
                                    min25color = Back.GREEN+min25result+Style.RESET_ALL
                                else:
                                    min25color = Back.RED+min25result+Style.RESET_ALL

                                if float(min30result[:-1]) > 0:
                                    min30color = Back.GREEN+min30result+Style.RESET_ALL
                                else:
                                    min30color = Back.RED+min30result+Style.RESET_ALL

                                if float(min35result[:-1]) > 0:
                                    min35color = Back.GREEN+min35result+Style.RESET_ALL
                                else:
                                    min35color = Back.RED+min35result+Style.RESET_ALL

                                if float(min40result[:-1]) > 0:
                                    min40color = Back.GREEN+min40result+Style.RESET_ALL
                                else:
                                    min40color = Back.RED+min40result+Style.RESET_ALL

                                if float(min45result[:-1]) > 0:
                                    min45color = Back.GREEN+min45result+Style.RESET_ALL
                                else:
                                    min45color = Back.RED+min45result+Style.RESET_ALL

                                if float(min50result[:-1]) > 0:
                                    min50color = Back.GREEN+min50result+Style.RESET_ALL
                                else:
                                    min50color = Back.RED+min50result+Style.RESET_ALL

                                if float(min55result[:-1]) > 0:
                                    min55color = Back.GREEN+min55result+Style.RESET_ALL
                                else:
                                    min55color = Back.RED+min55result+Style.RESET_ALL

                                m.add_row([x.upper(),min5color,min10color,min15color,min20color,min25color,min30color,min35color,min40color,min45color,min50color,min55color,countResult])

                        min5average = str(round(float(sum(min5results))/len(min5results),2))+"%"
                        min10average = str(round(float(sum(min10results))/len(min10results),2))+"%"
                        min15average = str(round(float(sum(min15results))/len(min15results),2))+"%"
                        min20average = str(round(float(sum(min20results))/len(min20results),2))+"%"
                        min25average = str(round(float(sum(min25results))/len(min25results),2))+"%"
                        min30average = str(round(float(sum(min30results))/len(min30results),2))+"%"
                        min35average = str(round(float(sum(min35results))/len(min35results),2))+"%"
                        min40average = str(round(float(sum(min40results))/len(min40results),2))+"%"
                        min45average = str(round(float(sum(min45results))/len(min45results),2))+"%"
                        min50average = str(round(float(sum(min50results))/len(min50results),2))+"%"
                        min55average = str(round(float(sum(min55results))/len(min55results),2))+"%"
                        countAverage = str(round(float(sum(countResults))/len(countResults),2))

                        if float(min5average[:-1]) > 0:
                            min5average = Back.GREEN+min5average+Style.RESET_ALL
                        else:
                            min5average = Back.RED+min5average+Style.RESET_ALL

                        if float(min10average[:-1]) > 0:
                            min10average = Back.GREEN+min10average+Style.RESET_ALL
                        else:
                            min10average = Back.RED+min10average+Style.RESET_ALL

                        if float(min15average[:-1]) > 0:
                            min15average = Back.GREEN+min15average+Style.RESET_ALL
                        else:
                            min15average = Back.RED+min15average+Style.RESET_ALL

                        if float(min20average[:-1]) > 0:
                            min20average = Back.GREEN+min20average+Style.RESET_ALL
                        else:
                            min20average = Back.RED+min20average+Style.RESET_ALL

                        if float(min25average[:-1]) > 0:
                            min25average = Back.GREEN+min25average+Style.RESET_ALL
                        else:
                            min25average = Back.RED+min25average+Style.RESET_ALL

                        if float(min30average[:-1]) > 0:
                            min30average = Back.GREEN+min30average+Style.RESET_ALL
                        else:
                            min30average = Back.RED+min30average+Style.RESET_ALL

                        if float(min35average[:-1]) > 0:
                            min35average = Back.GREEN+min35average+Style.RESET_ALL
                        else:
                            min35average = Back.RED+min35average+Style.RESET_ALL

                        if float(min40average[:-1]) > 0:
                            min40average = Back.GREEN+min40average+Style.RESET_ALL
                        else:
                            min40average = Back.RED+min40average+Style.RESET_ALL

                        if float(min45average[:-1]) > 0:
                            min45average = Back.GREEN+min45average+Style.RESET_ALL
                        else:
                            min45average = Back.RED+min45average+Style.RESET_ALL

                        if float(min50average[:-1]) > 0:
                            min50average = Back.GREEN+min50average+Style.RESET_ALL
                        else:
                            min50average = Back.RED+min50average+Style.RESET_ALL

                        if float(min55average[:-1]) > 0:
                            min55average = Back.GREEN+min55average+Style.RESET_ALL
                        else:
                            min55average = Back.RED+min55average+Style.RESET_ALL
                        

                        mAvg.add_row([min5average,min10average,min15average,min20average,min25average,min30average,min35average,min40average,min45average,min50average,min55average])
                        print()
                        print()
                        print()
                        print()
                        print()
                        print()
                        print()
                        print(">>> 5-MINUTE CHART <<<")
                        print(m)
                        print()
                        print(">>> AVERAGES <<<")
                        print(mAvg)
                        print()
                        print()
                        print()
                        print()
                        print()
                        print()
                        print()
            print(".", end="")
            time.sleep(60)

    # second menu option
    if choice == "2":
        # parse the RSS feed
        print()
        print()
        newsurl = ['http://www.bitnewz.net/rss/feed/15']
        feed = parseRSS( newsurl[0] )
        for newsitem in feed['items']: 
            title=newsitem['title']
            date=newsitem['published']

            # convert the timezone to US eastern
            fmt = "%m/%d/%Y %I:%M%p"
            tz = 'US/Eastern'
            d = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S Z')
            awareTime = pytz.utc.localize(d)
            easternTime = awareTime.astimezone(pytz.timezone(tz))
            dateFormatted = easternTime.strftime(fmt)

            # match the timestamp to the closest minute
            timestamp = int(d.strftime("%s"))
            mod=timestamp%60
            timestamp=timestamp-mod

            # make title only alphanumeric
            titleLower=title.lower()
            formattedTitle=""
            validLetters = "abcdefghijklmnopqrstuvwxyz0123456789 "
            for char in titleLower:
                if char in validLetters:
                    formattedTitle+=char

            # print title and date
            print(title.upper())
            print(dateFormatted)

            # minute and hour charts headers
            m = PrettyTable(['WORD', '5M', '10M', '15M', '20M', '25M', '30M', '35M', '40M', '45M', '50M', '55M', 'COUNT'])
            mAvg = PrettyTable(['5M', '10M', '15M', '20M', '25M', '30M', '35M', '40M', '45M', '50M', '55M'])

            words = formattedTitle.split()

            # arrays of results to later take an average of
            min5results=[]
            min10results=[]
            min15results=[]
            min20results=[]
            min25results=[]
            min30results=[]
            min35results=[]
            min40results=[]
            min45results=[]
            min50results=[]
            min55results=[]
            countResults=[]

            for x in words:
                if x in wordArray:
                    index = wordArray.index(x)

                    min5result = min5Array[index]
                    min10result = min10Array[index]
                    min15result = min15Array[index]
                    min20result = min20Array[index]
                    min25result = min25Array[index]
                    min30result = min30Array[index]
                    min35result = min35Array[index]
                    min40result = min40Array[index]
                    min45result = min45Array[index]
                    min50result = min50Array[index]
                    min55result = min55Array[index]
                    countResult = countArray[index]

                    min5color=""
                    min10color=""
                    min15color=""
                    min20color=""
                    min25color=""
                    min30color=""
                    min35color=""
                    min40color=""
                    min45color=""
                    min50color=""
                    min55color=""

                    min5results.append(float(min5result[:-1]))
                    min10results.append(float(min10result[:-1]))
                    min15results.append(float(min15result[:-1]))
                    min20results.append(float(min20result[:-1]))
                    min25results.append(float(min25result[:-1]))
                    min30results.append(float(min30result[:-1]))
                    min35results.append(float(min35result[:-1]))
                    min40results.append(float(min40result[:-1]))
                    min45results.append(float(min45result[:-1]))
                    min50results.append(float(min50result[:-1]))
                    min55results.append(float(min55result[:-1]))
                    countResults.append(int(countResult))

                    if float(min5result[:-1]) > 0:
                        min5color = Back.GREEN+min5result+Style.RESET_ALL
                    else:
                        min5color = Back.RED+min5result+Style.RESET_ALL

                    if float(min10result[:-1]) > 0:
                        min10color = Back.GREEN+min10result+Style.RESET_ALL
                    else:
                        min10color = Back.RED+min10result+Style.RESET_ALL

                    if float(min15result[:-1]) > 0:
                        min15color = Back.GREEN+min15result+Style.RESET_ALL
                    else:
                        min15color = Back.RED+min15result+Style.RESET_ALL

                    if float(min20result[:-1]) > 0:
                        min20color = Back.GREEN+min20result+Style.RESET_ALL
                    else:
                        min20color = Back.RED+min20result+Style.RESET_ALL

                    if float(min25result[:-1]) > 0:
                        min25color = Back.GREEN+min25result+Style.RESET_ALL
                    else:
                        min25color = Back.RED+min25result+Style.RESET_ALL

                    if float(min30result[:-1]) > 0:
                        min30color = Back.GREEN+min30result+Style.RESET_ALL
                    else:
                        min30color = Back.RED+min30result+Style.RESET_ALL

                    if float(min35result[:-1]) > 0:
                        min35color = Back.GREEN+min35result+Style.RESET_ALL
                    else:
                        min35color = Back.RED+min35result+Style.RESET_ALL

                    if float(min40result[:-1]) > 0:
                        min40color = Back.GREEN+min40result+Style.RESET_ALL
                    else:
                        min40color = Back.RED+min40result+Style.RESET_ALL

                    if float(min45result[:-1]) > 0:
                        min45color = Back.GREEN+min45result+Style.RESET_ALL
                    else:
                        min45color = Back.RED+min45result+Style.RESET_ALL

                    if float(min50result[:-1]) > 0:
                        min50color = Back.GREEN+min50result+Style.RESET_ALL
                    else:
                        min50color = Back.RED+min50result+Style.RESET_ALL

                    if float(min55result[:-1]) > 0:
                        min55color = Back.GREEN+min55result+Style.RESET_ALL
                    else:
                        min55color = Back.RED+min55result+Style.RESET_ALL

                    m.add_row([x.upper(),min5color,min10color,min15color,min20color,min25color,min30color,min35color,min40color,min45color,min50color,min55color,countResult])

            min5average = str(round(float(sum(min5results))/len(min5results),2))+"%"
            min10average = str(round(float(sum(min10results))/len(min10results),2))+"%"
            min15average = str(round(float(sum(min15results))/len(min15results),2))+"%"
            min20average = str(round(float(sum(min20results))/len(min20results),2))+"%"
            min25average = str(round(float(sum(min25results))/len(min25results),2))+"%"
            min30average = str(round(float(sum(min30results))/len(min30results),2))+"%"
            min35average = str(round(float(sum(min35results))/len(min35results),2))+"%"
            min40average = str(round(float(sum(min40results))/len(min40results),2))+"%"
            min45average = str(round(float(sum(min45results))/len(min45results),2))+"%"
            min50average = str(round(float(sum(min50results))/len(min50results),2))+"%"
            min55average = str(round(float(sum(min55results))/len(min55results),2))+"%"
            countAverage = str(round(float(sum(countResults))/len(countResults),2))

            if float(min5average[:-1]) > 0:
                min5average = Back.GREEN+min5average+Style.RESET_ALL
            else:
                min5average = Back.RED+min5average+Style.RESET_ALL

            if float(min10average[:-1]) > 0:
                min10average = Back.GREEN+min10average+Style.RESET_ALL
            else:
                min10average = Back.RED+min10average+Style.RESET_ALL

            if float(min15average[:-1]) > 0:
                min15average = Back.GREEN+min15average+Style.RESET_ALL
            else:
                min15average = Back.RED+min15average+Style.RESET_ALL

            if float(min20average[:-1]) > 0:
                min20average = Back.GREEN+min20average+Style.RESET_ALL
            else:
                min20average = Back.RED+min20average+Style.RESET_ALL

            if float(min25average[:-1]) > 0:
                min25average = Back.GREEN+min25average+Style.RESET_ALL
            else:
                min25average = Back.RED+min25average+Style.RESET_ALL

            if float(min30average[:-1]) > 0:
                min30average = Back.GREEN+min30average+Style.RESET_ALL
            else:
                min30average = Back.RED+min30average+Style.RESET_ALL

            if float(min35average[:-1]) > 0:
                min35average = Back.GREEN+min35average+Style.RESET_ALL
            else:
                min35average = Back.RED+min35average+Style.RESET_ALL

            if float(min40average[:-1]) > 0:
                min40average = Back.GREEN+min40average+Style.RESET_ALL
            else:
                min40average = Back.RED+min40average+Style.RESET_ALL

            if float(min45average[:-1]) > 0:
                min45average = Back.GREEN+min45average+Style.RESET_ALL
            else:
                min45average = Back.RED+min45average+Style.RESET_ALL

            if float(min50average[:-1]) > 0:
                min50average = Back.GREEN+min50average+Style.RESET_ALL
            else:
                min50average = Back.RED+min50average+Style.RESET_ALL

            if float(min55average[:-1]) > 0:
                min55average = Back.GREEN+min55average+Style.RESET_ALL
            else:
                min55average = Back.RED+min55average+Style.RESET_ALL
            

            mAvg.add_row([min5average,min10average,min15average,min20average,min25average,min30average,min35average,min40average,min45average,min50average,min55average])

            print()
            print(">>> 5-MINUTE CHART <<<")
            print(m)
            print()
            print(">>> AVERAGES <<<")
            print(mAvg)
            print()
            print()
            print()
            print()
            print()
            print()
            print()

    # third menu option
    if choice == "3":
        title = input("Please enter the word(s) or title of an article: ")

        # make title only alphanumeric
        titleLower=title.lower()
        formattedTitle=""
        validLetters = "abcdefghijklmnopqrstuvwxyz0123456789 "
        for char in titleLower:
            if char in validLetters:
                formattedTitle+=char

        # minute and hour charts headers
        m = PrettyTable(['WORD', '5M', '10M', '15M', '20M', '25M', '30M', '35M', '40M', '45M', '50M', '55M', 'COUNT'])
        mAvg = PrettyTable(['5M', '10M', '15M', '20M', '25M', '30M', '35M', '40M', '45M', '50M', '55M'])

        words = formattedTitle.split()

        # arrays of results to later take an average of
        min5results=[]
        min10results=[]
        min15results=[]
        min20results=[]
        min25results=[]
        min30results=[]
        min35results=[]
        min40results=[]
        min45results=[]
        min50results=[]
        min55results=[]
        countResults=[]

        for x in words:
            if x in wordArray:
                index = wordArray.index(x)

                min5result = min5Array[index]
                min10result = min10Array[index]
                min15result = min15Array[index]
                min20result = min20Array[index]
                min25result = min25Array[index]
                min30result = min30Array[index]
                min35result = min35Array[index]
                min40result = min40Array[index]
                min45result = min45Array[index]
                min50result = min50Array[index]
                min55result = min55Array[index]
                countResult = countArray[index]

                min5color=""
                min10color=""
                min15color=""
                min20color=""
                min25color=""
                min30color=""
                min35color=""
                min40color=""
                min45color=""
                min50color=""
                min55color=""

                min5results.append(float(min5result[:-1]))
                min10results.append(float(min10result[:-1]))
                min15results.append(float(min15result[:-1]))
                min20results.append(float(min20result[:-1]))
                min25results.append(float(min25result[:-1]))
                min30results.append(float(min30result[:-1]))
                min35results.append(float(min35result[:-1]))
                min40results.append(float(min40result[:-1]))
                min45results.append(float(min45result[:-1]))
                min50results.append(float(min50result[:-1]))
                min55results.append(float(min55result[:-1]))
                countResults.append(int(countResult))

                if float(min5result[:-1]) > 0:
                    min5color = Back.GREEN+min5result+Style.RESET_ALL
                else:
                    min5color = Back.RED+min5result+Style.RESET_ALL

                if float(min10result[:-1]) > 0:
                    min10color = Back.GREEN+min10result+Style.RESET_ALL
                else:
                    min10color = Back.RED+min10result+Style.RESET_ALL

                if float(min15result[:-1]) > 0:
                    min15color = Back.GREEN+min15result+Style.RESET_ALL
                else:
                    min15color = Back.RED+min15result+Style.RESET_ALL

                if float(min20result[:-1]) > 0:
                    min20color = Back.GREEN+min20result+Style.RESET_ALL
                else:
                    min20color = Back.RED+min20result+Style.RESET_ALL

                if float(min25result[:-1]) > 0:
                    min25color = Back.GREEN+min25result+Style.RESET_ALL
                else:
                    min25color = Back.RED+min25result+Style.RESET_ALL

                if float(min30result[:-1]) > 0:
                    min30color = Back.GREEN+min30result+Style.RESET_ALL
                else:
                    min30color = Back.RED+min30result+Style.RESET_ALL

                if float(min35result[:-1]) > 0:
                    min35color = Back.GREEN+min35result+Style.RESET_ALL
                else:
                    min35color = Back.RED+min35result+Style.RESET_ALL

                if float(min40result[:-1]) > 0:
                    min40color = Back.GREEN+min40result+Style.RESET_ALL
                else:
                    min40color = Back.RED+min40result+Style.RESET_ALL

                if float(min45result[:-1]) > 0:
                    min45color = Back.GREEN+min45result+Style.RESET_ALL
                else:
                    min45color = Back.RED+min45result+Style.RESET_ALL

                if float(min50result[:-1]) > 0:
                    min50color = Back.GREEN+min50result+Style.RESET_ALL
                else:
                    min50color = Back.RED+min50result+Style.RESET_ALL

                if float(min55result[:-1]) > 0:
                    min55color = Back.GREEN+min55result+Style.RESET_ALL
                else:
                    min55color = Back.RED+min55result+Style.RESET_ALL

                m.add_row([x.upper(),min5color,min10color,min15color,min20color,min25color,min30color,min35color,min40color,min45color,min50color,min55color,countResult])

        min5average = str(round(float(sum(min5results))/len(min5results),2))+"%"
        min10average = str(round(float(sum(min10results))/len(min10results),2))+"%"
        min15average = str(round(float(sum(min15results))/len(min15results),2))+"%"
        min20average = str(round(float(sum(min20results))/len(min20results),2))+"%"
        min25average = str(round(float(sum(min25results))/len(min25results),2))+"%"
        min30average = str(round(float(sum(min30results))/len(min30results),2))+"%"
        min35average = str(round(float(sum(min35results))/len(min35results),2))+"%"
        min40average = str(round(float(sum(min40results))/len(min40results),2))+"%"
        min45average = str(round(float(sum(min45results))/len(min45results),2))+"%"
        min50average = str(round(float(sum(min50results))/len(min50results),2))+"%"
        min55average = str(round(float(sum(min55results))/len(min55results),2))+"%"
        countAverage = str(round(float(sum(countResults))/len(countResults),2))

        if float(min5average[:-1]) > 0:
            min5average = Back.GREEN+min5average+Style.RESET_ALL
        else:
            min5average = Back.RED+min5average+Style.RESET_ALL

        if float(min10average[:-1]) > 0:
            min10average = Back.GREEN+min10average+Style.RESET_ALL
        else:
            min10average = Back.RED+min10average+Style.RESET_ALL

        if float(min15average[:-1]) > 0:
            min15average = Back.GREEN+min15average+Style.RESET_ALL
        else:
            min15average = Back.RED+min15average+Style.RESET_ALL

        if float(min20average[:-1]) > 0:
            min20average = Back.GREEN+min20average+Style.RESET_ALL
        else:
            min20average = Back.RED+min20average+Style.RESET_ALL

        if float(min25average[:-1]) > 0:
            min25average = Back.GREEN+min25average+Style.RESET_ALL
        else:
            min25average = Back.RED+min25average+Style.RESET_ALL

        if float(min30average[:-1]) > 0:
            min30average = Back.GREEN+min30average+Style.RESET_ALL
        else:
            min30average = Back.RED+min30average+Style.RESET_ALL

        if float(min35average[:-1]) > 0:
            min35average = Back.GREEN+min35average+Style.RESET_ALL
        else:
            min35average = Back.RED+min35average+Style.RESET_ALL

        if float(min40average[:-1]) > 0:
            min40average = Back.GREEN+min40average+Style.RESET_ALL
        else:
            min40average = Back.RED+min40average+Style.RESET_ALL

        if float(min45average[:-1]) > 0:
            min45average = Back.GREEN+min45average+Style.RESET_ALL
        else:
            min45average = Back.RED+min45average+Style.RESET_ALL

        if float(min50average[:-1]) > 0:
            min50average = Back.GREEN+min50average+Style.RESET_ALL
        else:
            min50average = Back.RED+min50average+Style.RESET_ALL

        if float(min55average[:-1]) > 0:
            min55average = Back.GREEN+min55average+Style.RESET_ALL
        else:
            min55average = Back.RED+min55average+Style.RESET_ALL
        

        mAvg.add_row([min5average,min10average,min15average,min20average,min25average,min30average,min35average,min40average,min45average,min50average,min55average])

        print()
        print()
        print()
        print()
        print()
        print()
        print(">>> 5-MINUTE CHART <<<")
        print(m)
        print()
        print(">>> AVERAGES <<<")
        print(mAvg)
        print()
        print()
        print()
        print()
        print()
        print()
        print()