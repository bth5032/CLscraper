#!/usr/bin/python

"""Written By: Bobak Hashemi
Last Updated: 6/26/14

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

username='GMAIL_USER' #gmail username
password='GMAIL_PASSWORD' #gmail password


#List of search URLs, can do an arbitrarily large number of queries so long as they fit in a python list
#Go to craigslist and do the search you want, then copy the URL string into the list, for instance
#http://sandiego.craigslist.org/search/apa?query=pacific+beach&sale_date=-&maxAsk=3500&bedrooms=4&hasPic=1
#would include a search for rentals in Pacific Beach with at least 4 bedrooms, posted with a picture, and charging under $3500 rent
urls = ['SEARCH_URL_1_HERE','SEARCH_URL_2_HERE','SEARCH_URL_3_HERE','SEARCH_URL_4_HERE']
### ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ SET ALL OF THESE BEFORE YOU START IT!!! ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



OldListings = [] #Initialize list of old posting's unique craigslist ID
email = [] #Initialize list of posting's to be emailed after some run.

new = False #Initialize flag to let program know whether there was a new listing


# ---- Start Initialization Run to get all posts already on craigslist
for craigslistLinkAddress in urls: 
	f = urllib.urlopen(craigslistLinkAddress) #Open Web Address

	soup = BeautifulSoup(f.read()) #read in html into BS4 data structure 

	content = str(soup.find_all("div", class_="content")[0]) #Don't really remember what this does

	soup = BeautifulSoup(content[:content.find("<h4 class=\"ban nearby\">")]) #Remove's the links from "nearby" towns that are far as fuck

	for listing in soup.find_all("p"): #For each listing
		if listing['data-pid'] not in OldListings: #check if listing is in the old list
			OldListings.append(listing['data-pid']) #add it to the old list if it's not there
			email.append(listing.find('a')['href']) #append the link to the list to be emailed
			new = True #let the program know there was a new posting

#Welcome message sent on first email
msg = "Hi ...! I will do your craigslist search every X minutes and notify you whenever a new house is posted that matches our search criteria. Here are all the intial positings that were up at the time your search was started... \n"
	
for listing in email: #construct the email message
	msg = msg+"http://sandiego.craigslist.org"+listing+'\n'


if new: #if there was a new post, send out an email
	server = smtplib.SMTP('smtp.gmail.com:587')  
	server.starttls()  
	server.login(username,password)  
	server.sendmail(fromaddr, toaddrs, msg)  
	server.quit() 


email = [] #re-initialize list of new posts and new post flag
new = False
	
time.sleep(SLEEPTIME) #wait for SLEEPTIME seconds before entering main loop


# ---- End Initialization Run
# ---- Start Main Loop

while True:
	print "\n\n "+str(datetime.datetime.now())+":  --Checking again!-- \n\n" #Print timestamp to terminal so you know it's working
	
	msg = "There are new postings: \n\n" #construct new message header

	for craigslistLinkAddress in urls: 
		f = urllib.urlopen(craigslistLinkAddress) #Open Web Address

		soup = BeautifulSoup(f.read()) #read in html into BS4 data structure 

		content = str(soup.find_all("div", class_="content")[0]) #Don't really remember what this does

		soup = BeautifulSoup(content[:content.find("<h4 class=\"ban nearby\">")]) #Remove's the links from "nearby" towns that are far as fuck

		for listing in soup.find_all("p"): #For each listing
			if listing['data-pid'] not in OldListings:  #check if listing is in the old list
				OldListings.append(listing['data-pid']) #add it to the old list if it's not there
				email.append(listing.find('a')['href']) #append the link to the list to be emailed
				new = True #let the program know there was a new posting


	for listing in email: #construct the email message
		msg = msg+"http://sandiego.craigslist.org"+listing+'\n'

	msg = msg+"\n\n Hope there were some good ones!" #email footer
		
	if new: #if there was a new post, send out an email 
		server = smtplib.SMTP('smtp.gmail.com:587')  
		server.starttls()  
		server.login(username,password)  
		server.sendmail(fromaddr, toaddrs, msg)  
		server.quit() 

	#re-initialize list of new posts and new post flag and wait SLEEPTIME seconds before starting again
	email = []
	new = False
	time.sleep(SLEEPTIME)
