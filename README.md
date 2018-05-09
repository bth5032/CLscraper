# CLscraper

A simple script that will send you emails when a craigslist search query gets new results, i.e. when something new is posted that matches your search criteria.

The program uses the Beautiful Soup package, to install run

```bash
sudo easy_install beautifulsoup4
```

Additionally, this program uses gmail to send email messages. You must set up your gmail account to work with "less secure apps" [here](https://myaccount.google.com/lesssecureapps?pli=1)

You can also make a new gmail account to do this if your main one has two factor authentification or you generally want stronger security.

## Usage
To use the program, first go to craigslist and search for whatever you are looking for, then replace the tokens for URLs in CLscrapper.py with the URLs for the searches of insterest. 

For instance, if you want an apartment in Pacific Beach, San Diego with at least 4 bedrooms and costing less than 3500 per month, the craigslist search string will be

```
https://sandiego.craigslist.org/search/apa?sort=date&availabilityMode=0&hasPic=1&max_price=3500&min_bedrooms=4&query=pacific%20beach
```

The same search in La Jolla, CA would be 

```
https://sandiego.craigslist.org/search/apa?sort=date&availabilityMode=0&hasPic=1&max_price=3500&min_bedrooms=4&query=la%20jolla
```

In this example, replace 

```python 
urls = ['SEARCH_URL_1_HERE','SEARCH_URL_2_HERE','SEARCH_URL_3_HERE','SEARCH_URL_4_HERE']
```

with

```python 
urls = ['https://sandiego.craigslist.org/search/apa?sort=date&availabilityMode=0&hasPic=1&max_price=3500&min_bedrooms=4&query=pacific%20beach', 'https://sandiego.craigslist.org/search/apa?sort=date&availabilityMode=0&hasPic=1&max_price=3500&min_bedrooms=4&query=la%20jolla']
```
**Note:** For searches with a lot of results, they will not all load on one page. To remedey this, make sure you have sorted the page by 'newest', which will be reflected in the URL as of May 2018 with the token `sort=date`. The default page count is 120, so as long as there are not 120 new posts within the time between searches, set by `SLEEPTIME`, you should still catch them all. But generally, this means it's better to use many specific searches than one broad search.


You can use any number of searches for any number of different things. By default, the code is configured to use send email updates using a gmail account. If you have a gmail account, you can simply replace the lines

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

with a list of email addresses that should get the updates. You can make this list as long as you want. It's also fine to just email yourself, but this needs to stay a list.

The last two configurables are `SLEEP_TIME` and `CHECK_OLD_LISTINGS`. `SLEEP_TIME` is the number of seconds between searches, and `CHECK_OLD_LISTINGS` attempts to not send reposted listings. 

This program must stay alive to work properly, you will need a machine that can stay on and connected to the internet. Run with

```bash
python CLscraper.py
```