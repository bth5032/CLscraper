# CLscraper

A simple script that will send you emails when a craigslist search query gets new results, i.e. when something new is posted that matches your search criteria.

The program uses the Beautiful Soup package, to install run

```bash
sudo easy_install beautifulsoup4
```
## Usage
To use the program, first go to craigslist and search for whatever you are looking for, then replace the tokens for URLs in CLscrapper.py with the URLs for the searches of insterest. 

For instance, if you want an apartment in Pacific Beach, San Diego with at least 4 bedrooms and costing less than 3500 per month, the craigslist search string will be

```
https://sandiego.craigslist.org/search/apa?query=pacific+beach&hasPic=1&max_price=3500&min_bedrooms=4&availabilityMode=0&sale_date=all+dates
```

The same search in La Jolla, CA would be 

```
https://sandiego.craigslist.org/search/apa?query=la+jolla&hasPic=1&max_price=3500&min_bedrooms=4&availabilityMode=0&sale_date=all+dates
```

In this example, replace 

```python 
urls = ['SEARCH_URL_1_HERE','SEARCH_URL_2_HERE','SEARCH_URL_3_HERE','SEARCH_URL_4_HERE']
```

with

```python 
urls = ['https://sandiego.craigslist.org/search/apa?query=pacific+beach&hasPic=1&max_price=3500&min_bedrooms=4&availabilityMode=0&sale_date=all+dates', 'https://sandiego.craigslist.org/search/apa?query=la+jolla&hasPic=1&max_price=3500&min_bedrooms=4&availabilityMode=0&sale_date=all+dates']
```

By default, the code is configured to use send email updates using a gmail account. If you have a gmail account, you can simply replace the lines

```python
username='GMAIL_USER' #gmail username
password='GMAIL_PASSWORD' #gmail password
```

with your login credentials and replace 

```python 
fromaddr = 'EMAIL@ADDR.COM'
```
with your gmail address. Then update 

```python 
toaddrs = ['EMAIL1@ADDR.COM', 'EMAIL2@ADDR.COM', 'EMAIL3@ADDR.COM', 'EMAIL4@ADDR.COM']
```

with a list of email addresses that should get the updates. It's totally fine to just email yourself, but this needs to stay a list.

The last two configurables are `SLEEP_TIME` and `CHECK_OLD_LISTINGS`. `SLEEP_TIME` is the number of seconds between searches, and `CHECK_OLD_LISTINGS` attempts to not send reposted listings. 

This program must stay alive to work properly, you will need a machine that can stay on and connected to the internet. Run with

```bash
python CLscraper.py
```