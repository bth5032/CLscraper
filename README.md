# CLscraper

A simple Python script that will send you emails when a craigslist search query gets new results, i.e. when something new is posted that matches your search criteria.


## Install 

```bash
git clone https://github.com/bth5032/CLscraper
cd CLscraper
pip install -r requirements.txt
```

Additionally, to use Gmail servers, You must set up your gmail account to work with "less secure apps" [here](https://myaccount.google.com/lesssecureapps?pli=1).  
You can also make a new gmail account to do this if your main one has two factor authentification or you generally want stronger security.

## Configure
Open `config.ini` file and setup mail sever settings.

Then go to craigslist and search for whatever you are looking for, then replace the tokens with the URLs for the searches of insterest. 

For instance, if you want an apartment in Pacific Beach, San Diego with at least 4 bedrooms and costing less than 3500 per month, the craigslist search string will be

```
https://sandiego.craigslist.org/search/apa?sort=date&availabilityMode=0&hasPic=1&max_price=3500&min_bedrooms=4&query=pacific%20beach
```

The same search in La Jolla, CA would be 

```
https://sandiego.craigslist.org/search/apa?sort=date&availabilityMode=0&hasPic=1&max_price=3500&min_bedrooms=4&query=la%20jolla
```

In this example, url list will look like 

```
urls = ["https://sandiego.craigslist.org/search/apa?sort=date&availabilityMode=0&hasPic=1&max_price=3500&min_bedrooms=4&query=pacific%20beach", "https://sandiego.craigslist.org/search/apa?sort=date&availabilityMode=0&hasPic=1&max_price=3500&min_bedrooms=4&query=la%20jolla"]
```
**Note:** For searches with a lot of results, they will not all load on one page. To remedey this, make sure you have sorted the page by 'newest', which will be reflected in the URL as of May 2018 with the token `sort=date`. The default page count is 120, so as long as there are not 120 new posts within the time between searches, set by `SLEEPTIME`, you should still catch them all. But generally, this means it's better to use many specific searches than one broad search.

The final config option is the `sleeptime` mentioned above. This is the interval between searches in minutes. The default option is `[1,10]`, meaning that the script will check craigslist at a random time between 1 and 10 minutes. If you make this number too small, then craigslist will ban your IP.

You can also configure `CHECK_OLD_LISTINGS` in the script itself. If the `CHECK_OLD_LISTINGS` flag is set (it is by default), then the script attempts to not send reposted listings.

This program must stay alive to work properly, you will need a machine that can stay on and connected to the internet. Run with

```bash
python CLscraper.py
```