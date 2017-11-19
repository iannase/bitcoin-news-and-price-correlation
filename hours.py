# Ian Annase
# 11/19/17

import feedparser
from datetime import datetime
import csv
import pytz
import xlsxwriter
 
# function to fetch the rss feed and return the parsed rss
def parseRSS( rss_url ):
    return feedparser.parse( rss_url ) 

# parse the csv file into arrays
priceArray=[]
timestampArray=[]
allWords = []
hourChanges=[]
twoHourChanges=[]
threeHourChanges=[]
fourHourChanges=[]
fiveHourChanges=[]
sixHourChanges=[]
zz=0

# create excel file
excelWorkbook = xlsxwriter.Workbook('results.xlsx')
excelSheet = excelWorkbook.add_worksheet()
bold = excelWorkbook.add_format({'bold': True})
excelSheet.write('A1',"Word",bold)
excelSheet.write('B1',"Hour 1",bold)
excelSheet.write('C1',"Hour 2",bold)
excelSheet.write('D1',"Hour 3",bold)
excelSheet.write('E1',"Hour 4",bold)
excelSheet.write('F1',"Hour 5",bold)
excelSheet.write('G1',"Hour 6",bold)

# open CSV
with open('coinbase.csv','r') as csv_file:
    csv_reader = csv.reader(csv_file)
    print()
    print("Loading array and news articles...")
    for line in csv_reader:
        timestampArray.append(line[0])
        priceArray.append(line[1])

z=1
# parse the RSS feed
newsurl = ['http://www.bitnewz.net/rss/feed/100000']
feed = parseRSS( newsurl[0] )
for newsitem in feed['items']: 
    title=newsitem['title']
    date=newsitem['published']
    link=newsitem['link']

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
    print(title)
    print(dateFormatted)

    # make sure the article can be used with the dataset
    if timestamp < 1508064660 and timestamp > 1422748800:
        zz+=1
        priceAtPost=0
        hour=0
        twoHour=0
        threeHour=0
        fourHour=0
        fiveHour=0
        sixHour=0

        try:
            index = timestampArray.index(str(timestamp))
            priceAtPost=priceArray[index]
            index = timestampArray.index(str(timestamp+60*60))
            hour=priceArray[index]
            index = timestampArray.index(str(timestamp+120*60))
            twoHour=priceArray[index]
            index = timestampArray.index(str(timestamp+180*60))
            threeHour=priceArray[index]
            index = timestampArray.index(str(timestamp+240*60))
            fourHour=priceArray[index]
            index = timestampArray.index(str(timestamp+300*60))
            fiveHour=priceArray[index]
            index = timestampArray.index(str(timestamp+360*60))
            sixHour=priceArray[index]
        except ValueError:
            continue

        hourChange = round(((float(hour)-float(priceAtPost))/float(priceAtPost)*100),2)
        twoHourChange = round(((float(twoHour)-float(priceAtPost))/float(priceAtPost)*100),2)
        threeHourChange = round(((float(threeHour)-float(priceAtPost))/float(priceAtPost)*100),2)
        fourHourChange = round(((float(fourHour)-float(priceAtPost))/float(priceAtPost)*100),2)
        fiveHourChange = round(((float(fiveHour)-float(priceAtPost))/float(priceAtPost)*100),2)
        sixHourChange = round(((float(sixHour)-float(priceAtPost))/float(priceAtPost)*100),2)

        words = formattedTitle.split()
        for j in words:
            allWords.append(j)
            hourChanges.append(hourChange)
            excelSheet.write(z,0,j)
            excelSheet.write(z,1,hourChange)
            excelSheet.write(z,2,twoHourChange)
            excelSheet.write(z,3,threeHourChange)
            excelSheet.write(z,4,fourHourChange)
            excelSheet.write(z,5,fiveHourChange)
            excelSheet.write(z,6,sixHourChange)
            z+=1

        if z > 1000001:
            excelWorkbook.close()
            break

        if hourChange > 0:
            print("Hour:\t\t^ " + str(hourChange)+"% ^")
        else:
            print("Hour:\t\tv " + str(hourChange)+"% v")

    print()
    


zipped = zip(allWords,hourChanges)
for x in zipped:
    print(x)

print("Results: " + str(zz))
print("Words: " + str(len(allWords)))

# close and save the excel workbook
excelWorkbook.close()
