# HTML tutorial https://www.w3schools.com/html/default.asp
from bs4 import BeautifulSoup
import re
import time
import requests
import csv

def run(url,pageNum):

    fw=open('ads.txt','w',encoding='utf8') # output file

    writer=csv.writer(fw,lineterminator='\n')#create a csv writer to write the job ad text and job type for each job
    
    for list_page in range(0,pageNum-1): # for each page 
        
        print ('page', list_page)
        html=None

        if list_page == 1: 
            pageLink=url # url for page 1
        else:
            pageLink=url+'&start='+str(list_page*10) # make the page url

        for i in range(5): # try 5 times

            # send a request to access the url
            response=requests.get(pageLink,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
            if response: # explanation on response codes: https://realpython.com/python-requests/#status-codes
                break # we got the file, break the loop
            else: time.sleep(2) # wait 2 secs
            
   
        # all five attempts failed, return  None
        if not response: 
            return None
    
        list_html = response.text # read in the html
        
        listSoup = BeautifulSoup(list_html,'html') # parse the html

        jobs = listSoup.findAll('a', {'target':'_blank', 'data-tn-element':'jobTitle'}) # get the <a> tag that contains the url for each job
        
        for jobAd in jobs:
            jobURL = str("https://www.indeed.com" + jobAd.get("href"))
            print(jobURL)

            for i in range(5): # try 5 times
                # send a request to access the jobURL
                response = requests.get(jobURL ,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                if response: # explanation on response codes: https://realpython.com/python-requests/#status-codes
                    break # we got the file, break the loop
                else: time.sleep(2) # wait 2 secs
                
            # all five attempts failed, return  None
            if not response: 
                return None
                
            job_html = response.text # read in the job html

            #TODO: save the html for each ad into a folder

            jobSoup = BeautifulSoup(job_html, 'html')

            job_description = jobSoup.find('div', {'id':'jobDescriptionText'})

            print(job_description.get_text())

            #TODO: save as line into csv with jobtype nexxt to it

                

        """
        for review in reviews:

            critic, rating, source, text, date ='NA','NA','NA','NA','NA' # initialize critic and text 
            
            criticChunk = review.find('a',{'href':re.compile('/critic/')})
            if criticChunk: critic=criticChunk.text.strip()
            
            ratingChunk = review.find('div', {'class':re.compile('review_icon')})
            if ratingChunk:
                if 'fresh' in str(ratingChunk): rating = 'fresh'
                else: rating = 'rotten'
                
            sourceChunk = review.find('em', {'class':'subtle critic-publication'})
            if sourceChunk: source = sourceChunk.text.strip()
                            
            textChunk=review.find('div',{'class':'the_review'})
            if textChunk: text = textChunk.text.strip()
            
            dateChunk = review.find('div', {'class': 'review-date subtle small'})
            if dateChunk: date = dateChunk.text.strip()            
            
            writer.writerow([critic, rating, source, text, date]) # write to file 
            """            
    print("finished")
    fw.close()


url= 'https://www.indeed.com/jobs?q=data+engineer&l=Washington,+DC&radius=100&fromage=last&start=0'
run(url,3)