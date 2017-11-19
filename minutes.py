# Ian Annase
# 11/19/2017

from datetime import datetime
import feedparser
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
excelWorkbook = xlsxwriter.Workbook('results/minutes_results.xlsx')
excelSheet = excelWorkbook.add_worksheet()
bold = excelWorkbook.add_format({'bold': True})
excelSheet.write('A1',"Word",bold)
excelSheet.write('B1',"5 Min",bold)
excelSheet.write('C1',"10 Min",bold)
excelSheet.write('D1',"15 Min",bold)
excelSheet.write('E1',"20 Min",bold)
excelSheet.write('F1',"25 Min",bold)
excelSheet.write('G1',"30 Min",bold)
excelSheet.write('H1',"35 Min",bold)
excelSheet.write('I1',"40 Min",bold)
excelSheet.write('J1',"45 Min",bold)
excelSheet.write('K1',"50 Min",bold)
excelSheet.write('L1',"55 Min",bold)
excelSheet.write('M1',"60 Min",bold)

# open CSV
with open('data/coinbase.csv','r') as csv_file:
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
        min5=0
        min10=0
        min15=0
        min20=0
        min25=0
        min30=0
        min35=0
        min40=0
        min45=0
        min50=0
        min55=0
        min60=0

        try:
            index = timestampArray.index(str(timestamp))
            priceAtPost=priceArray[index]
            index = timestampArray.index(str(timestamp+5*60))
            min5=priceArray[index]
            index = timestampArray.index(str(timestamp+10*60))
            min10=priceArray[index]
            index = timestampArray.index(str(timestamp+15*60))
            min15=priceArray[index]
            index = timestampArray.index(str(timestamp+20*60))
            min20=priceArray[index]
            index = timestampArray.index(str(timestamp+25*60))
            min25=priceArray[index]
            index = timestampArray.index(str(timestamp+30*60))
            min30=priceArray[index]
            index = timestampArray.index(str(timestamp+35*60))
            min35=priceArray[index]
            index = timestampArray.index(str(timestamp+40*60))
            min40=priceArray[index]
            index = timestampArray.index(str(timestamp+45*60))
            min45=priceArray[index]
            index = timestampArray.index(str(timestamp+50*60))
            min50=priceArray[index]
            index = timestampArray.index(str(timestamp+55*60))
            min55=priceArray[index]
            index = timestampArray.index(str(timestamp+60*60))
            min60=priceArray[index]
            sixHour=priceArray[index]
        except ValueError:
            continue

        min5change = round(((float(min5)-float(priceAtPost))/float(priceAtPost)*100),2)
        min10change = round(((float(min10)-float(priceAtPost))/float(priceAtPost)*100),2)
        min15change = round(((float(min15)-float(priceAtPost))/float(priceAtPost)*100),2)
        min20change = round(((float(min20)-float(priceAtPost))/float(priceAtPost)*100),2)
        min25change = round(((float(min25)-float(priceAtPost))/float(priceAtPost)*100),2)
        min30change = round(((float(min30)-float(priceAtPost))/float(priceAtPost)*100),2)
        min35change = round(((float(min35)-float(priceAtPost))/float(priceAtPost)*100),2)
        min40change = round(((float(min40)-float(priceAtPost))/float(priceAtPost)*100),2)
        min45change = round(((float(min45)-float(priceAtPost))/float(priceAtPost)*100),2)
        min50change = round(((float(min50)-float(priceAtPost))/float(priceAtPost)*100),2)
        min55change = round(((float(min55)-float(priceAtPost))/float(priceAtPost)*100),2)
        min60change = round(((float(min60)-float(priceAtPost))/float(priceAtPost)*100),2)

        words = formattedTitle.split()
        for j in words:
            allWords.append(j)
            hourChanges.append(min10change)
            excelSheet.write(z,0,j)
            excelSheet.write(z,1,min5change)
            excelSheet.write(z,2,min10change)
            excelSheet.write(z,3,min15change)
            excelSheet.write(z,4,min20change)
            excelSheet.write(z,5,min25change)
            excelSheet.write(z,6,min30change)
            excelSheet.write(z,7,min35change)
            excelSheet.write(z,8,min40change)
            excelSheet.write(z,9,min45change)
            excelSheet.write(z,10,min50change)
            excelSheet.write(z,11,min55change)
            excelSheet.write(z,12,min60change)
            z+=1

        if z > 1000001:
            excelWorkbook.close()
            break

        if min10change > 0:
            print("10 Min:\t\t^ " + str(min10change)+"% ^")
        else:
            print("10 Min:\t\tv " + str(min10change)+"% v")
    print()
print("Results: " + str(zz))
print("Words: " + str(len(allWords)))

# close and save the excel workbook
excelWorkbook.close()
