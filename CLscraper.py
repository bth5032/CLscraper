#!/usr/bin/python

"""Written By: Bobak Hashemi
Last Updated: 5/9/2018

This program takes in a list of craigslist search queries (given by the search links with GET data), 
indexes the results for each query, and emails new posts to a set of specified email addresses. 

This program uses the beautiful soup 4 package, to install run "sudo easy_install beautifulsoup4"
 """

import urllib
import datetime
from bs4 import BeautifulSoup
import time
import smtplib

### vvvvvvvvvvvvvvvvvvvvvvvvvvvv SET ALL OF THESE BEFORE YOU START IT!!! vvvvvvvvvvvvvvvvvvvvvvvvvvvv
fromaddr = 'EMAIL@ADDR.COM' #Email address that the email is recieved from
toaddrs = ['EMAIL1@ADDR.COM', 'EMAIL2@ADDR.COM', 'EMAIL3@ADDR.COM', 'EMAIL4@ADDR.COM'] #List of addresses to send the links to
SLEEPTIME = 300 #number of seconds between searches
CHECK_OLD_LISTINGS = True #If True, don't resend listings that have been reposted

username='GMAIL_USER' #gmail username
password='GMAIL_PASSWORD' #gmail password


#List of search URLs, can do an arbitrarily large number of queries so long as they fit in a python list
#Go to craigslist and do the search you want, then copy the URL string into the list, for instance
#https://sandiego.craigslist.org/search/apa?query=pacific+beach&sort=date&hasPic=1&max_price=3500&availabilityMode=0&sale_date=all+dates
#would include a search for rentals in Pacific Beach with at least 4 bedrooms, posted with a picture, and charging under $3500 rent
#make sure you sort the page by newest so that sort=date shows up in the URL. The default page count is 120, so as long as there are not
#120 new posts within SLEEPTIME you should still catch them all. But generally, this means it's better to use many specific searches than one broad search.
urls = ['SEARCH_URL_1_HERE','SEARCH_URL_2_HERE','SEARCH_URL_3_HERE','SEARCH_URL_4_HERE']
### ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ SET ALL OF THESE BEFORE YOU START IT!!! ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

old_listings = [] #Initialize list of old posting's unique craigslist ID
email = [] #Initialize list of posting's to be emailed after some run.

def constructMessage(msg, new_listings):
	"""Constructs the message given the message head and the list of new postings"""
	for pid in new_listings.keys(): #construct the email message
			msg = msg+"<a href=\""+new_listings[pid][0]+"\">"+new_listings[pid][1]+"</a>\n"
	return msg

def getListOfIdsAndUrls():	
	"""Scrapes the web pages for listings and returns a dictionary with PIDs as keys and (URLs, title) as value for stuff not in old_listings"""
	new_listings = {} #dictionary which holds the unique ID for each listing and the URL.

	for craigslistLinkAddress in urls: 
			f = urllib.urlopen(craigslistLinkAddress) #Open Web Address

			soup = BeautifulSoup(f.read(),"html.parser") #read in html into BS4 data structure 

			content = str(soup.find_all("div", class_="content")[0]) #Get the body of the search, strips away all the sidebars and stuff.

			soup = BeautifulSoup(content[:content.find("<h4 class=\"ban nearby\">")],"html.parser") #Remove's the links from "nearby" towns that are far away

			for listing in soup.find_all("li", {"class": "result-row"}): #For each listing, find the listings by searching for results table elements. This tag also stores a unique ID for each listing
				#grad the unique ID and URL for the listing, CHECK_OLD_LISTINGS is set, it also checks the repost of ID against the old_listings list.
				pid = listing.attrs["data-pid"]	
				old_pid = pid
				url = listing.find("a", {"class": "result-title"}).attrs["href"] #finds the link by looking for a link with results-title class and extracts the url.
				title = listing.find("a", {"class": "result-title"}).text        #finds the listing title
				if CHECK_OLD_LISTINGS:
					if "data-repost-of" in listing.attrs.keys():
						old_pid = listing.attrs["data-repost-of"]

				if (pid not in old_listings) and (old_pid not in old_listings): #check if listing is in the old list
					new_listings[pid] = (url, title)        #listing should be returned
					old_listings.append(pid)       #add the new pid to list of ones we've seen
					old_listings.append(old_pid)   #add the old pid to list of ones we've seen for future proofing

				elif (pid not in old_listings):
					old_listings.append(pid)       #I'm not sure if the old PID gets updated when someone reposts, or if it stays as the very first PID the listing was ever posted as. This should take care of the former case.

	return new_listings

def doIteration(msg):	
	new_listings = getListOfIdsAndUrls()
	
	if new_listings:
		msg = constructMessage(msg, new_listings)
		print "Found new listings, about to send email: \n%s" % msg

		server = smtplib.SMTP('smtp.gmail.com:587')  
		server.starttls()  
		server.login(username,password)  
		server.sendmail(fromaddr, toaddrs, msg)  
		server.quit() 
	else:
		print "No new listings found"

# ---- Start Initialization Run to get all posts already on craigslist
#Welcome message sent on first email
msg = "Hi ...! I will do your craigslist search every X minutes and notify you whenever a new house is posted that matches our search criteria. Here are all the intial positings that were up at the time your search was started... \n"
doIteration(msg)
email = [] #re-initialize list of new posts and new post flag
new = False	
time.sleep(SLEEPTIME) #wait for SLEEPTIME seconds before entering main loop


# ---- End Initialization Run
# ---- Start Main Loop

while True:
	print "\n\n "+str(datetime.datetime.now())+":  --Checking again!-- \n\n" #Print timestamp to terminal so you know it's working
	
	msg = "There are new postings: \n\n" #construct new message header
	doIteration(msg)
	#re-initialize list of new posts and new post flag and wait SLEEPTIME seconds before starting again
	email = []
	new = False
	time.sleep(SLEEPTIME)
