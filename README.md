##Bitcoin News and Price Correlation

![](https://ianannasetech.files.wordpress.com/2017/11/screen-shot-2017-11-19-at-2-43-17-am.png?w=1536)

> How do the titles of news articles affect the price of bitcoin?

###Prerequisites

For this project, I wanted to see how the titles of news articles about bitcoin affect its price. I analyzed 500,000 words from 50,000 article titles related to bitcoin. In order to do this I needed a few things:

- A list of the past three years of Bitcoin prices down to the minute
- An RSS feed that had a long history of articles
- A database to quickly summarize data

I found an awesome website ([Kaggle](https://www.kaggle.com/mczielinski/bitcoin-historical-data "Kaggle")) that had a CSV of all the past bitcoin prices minute-by-minute to the beginning of 2015. I also found a website that would give me the RSS feed required ([BitNewz](http://bitnewz.net/Articles "BitNewz")).

![](https://ianannasetech.files.wordpress.com/2017/11/screen-shot-2017-11-19-at-2-40-24-am.png?w=1536)

###Retrieving data about 100,000 articles (minutes.py)
Now that I had my dataset, I started by parsing all of the data from the CSV file into my program. After that, I parsed the RSS feed for the last 50,000 articles about bitcoin. The titles of all 50,000 were then divided up into their individual words.

![](https://ianannasetech.files.wordpress.com/2017/11/gif.gif?w=600&zoom=2)

###Exporting the data to Excel
I used the timestamps of the articles in order to find the same timestamp in the parsed CSV file. Then I added specific amounts to the timestamp in order to find out the difference in price after the article was posted. I did this for 5-minute intervals all the way up to 55 minutes. This data was being appended to an excel file as it was running through the articles.

![](https://ianannasetech.files.wordpress.com/2017/11/screen-shot-2017-11-18-at-1-36-23-pm.png)

### Microsoft Access (Summarizing the data)

Next, I opened up this excel file with over 500,000 records in Microsoft Access. I ran a query on this data in order to consolidate all of the words that were the same and get an average price change for each word. After running the query, I was left with about 26,000 records in the dataset. I immediately noticed some interesting numbers. For example, whenever the word “CEO” was mentioned in an article, the price of bitcoin went on a downward trend.

![](https://ianannasetech.files.wordpress.com/2017/11/screen-shot-2017-11-19-at-2-42-00-am.png?w=1536)

### The final dataset (26,000 unique words) (input.csv)
After that, I exported these records back to excel. This is the excel file that I used in order to make price predictions for new articles.

###Analyzing new articles based on the dataset (checker.py)

The final python program gives users a few choices, they can:

1. Turn on an RSS monitor that will notify them whenever a new article comes out, as well as give them a price prediction based on the title of that article.
2. View the 15 most recent articles posted online about bitcoin, and see what the price predictions were for those.
3. Enter their own title/keywords and see what the price predictions would be.

![](https://ianannasetech.files.wordpress.com/2017/11/screen-shot-2017-11-19-at-2-35-51-am.png?w=1536)

![](https://ianannasetech.files.wordpress.com/2017/11/screen-shot-2017-11-19-at-2-44-04-am.png?w=1536)

![](https://ianannasetech.files.wordpress.com/2017/11/screen-shot-2017-11-19-at-2-44-18-am.png)
