"""
This file contains a run function that takes as input the link to an indeed.com list of jobs, and returns a csv with <jobtext>,<jobtype>.
"""

from bs4 import BeautifulSoup
import re
import time
import requests
import csv
import os
import io

def run_scraper(url,page_num, job_type):

    csv_file=open('ads.csv','w',encoding='utf8') # creates and opens a file called ads.txt to place the <jobtext>,<jobtype> one per line

    writer=csv.writer(csv_file,delimiter=",", lineterminator='\n') # create a csv writer to write the job ad text and job type for each job
    
    visited_jobs = set()

    for list_page in range(0,page_num): # for each page 
        
        print ('Scraping page', str(list_page+1))

        page_link=url+'&start='+str(list_page*10) # make the page url for each page

        for i in range(5): # try 5 times in case connection drops momentarily
            # send a request to access the url
            response=requests.get(page_link,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
            if response: # explanation on response codes: https://realpython.com/python-requests/#status-codes
                break # we got the file, break the loop
            else: time.sleep(2) # wait 2 secs

        # all five attempts failed, return  None
        if not response: 
            return None
    
        list_html = response.text # read in the html of the website ontaining the list of jobs
        
        list_soup = BeautifulSoup(list_html,'html') # parse the html using BS so we can get the links to the specific jobs' sites

        jobs = list_soup.findAll('a', {'target':'_blank', 'data-tn-element':'jobTitle'}) # get a list of all the <a> tags that contain the url for each job
        
        for job_idx, job_ad in enumerate(jobs):
            print("Processing job #", job_idx, "from page", str(list_page+1))
            job_url = str("https://www.indeed.com" + job_ad.get("href")) # complete the url since only the tail of it is given

            if job_url in visited_jobs:
                continue

            for i in range(5): # try 5 times
                # send a request to access the job_url
                response = requests.get(job_url ,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                if response: # explanation on response codes: https://realpython.com/python-requests/#status-codes
                    break # we got the file, break the loop
                else: time.sleep(2) # wait 2 secs
            # all five attempts failed, return  None
            if not response:
                print("The request to get webpage has failed") 
                return None
                
            job_html = response.text # read in the job html (this is the job page that contains the full text description)

            # as per the deliverables, save the html for each job
            current_dir = os.path.dirname(os.path.realpath(__file__))
            if not os.path.exists(os.path.join(current_dir, str("jobs/" + job_type))):
                os.makedirs(os.path.join(current_dir, str("jobs/"+job_type)))
            
            with io.open("jobs/" + str(job_type) + "/page_" + str(list_page+1) + "_job_" + str(job_idx+1) , "w", encoding="utf-8") as html_file:
                html_file.write(job_html)
                html_file.close()

            jobSoup = BeautifulSoup(job_html, 'html') # parse the html of the job using beautiful soup so we can retrieve the relevant text

            job_description = jobSoup.find('div', {'id':'jobDescriptionText'}) #find the description of the job 
            if job_description != None:
                writer.writerow([job_description.get_text(), job_type])
            
            visited_jobs.add(job_url)

            
    print("finished")
    csv_file.close()


run_scraper("https://www.indeed.com/jobs?q=Data+Engineer&l=Washington%2C+DC&radius=100", 990, "data engineer")
run_scraper("https://www.indeed.com/jobs?q=data+engineer&l=Princeton%2C+NJ&radius=100", 990, "data engineer")
run_scraper("https://www.indeed.com/jobs?q=data+engineer&l=Sacramento%2C+CA&radius=100", 980, "data engineer")
run_scraper("https://www.indeed.com/jobs?q=software+engineer&l=Washington%2C+DC&radius=100", 940, "software engineer")
run_scraper("https://www.indeed.com/jobs?q=software+engineer&l=Princeton%2C+NJ&radius=100", 930, "software engineer")
run_scraper("https://www.indeed.com/jobs?q=software+engineer&l=Sacramento%2C+CA&radius=100", 990, "software engineer")
run_scraper("https://www.indeed.com/jobs?q=data+scientist&l=Washington%2C+DC&radius=100", 690, "data scientist")
run_scraper("https://www.indeed.com/jobs?q=data+scientist&l=Princeton%2C+NJ&radius=100", 670, "data scientist")
run_scraper("https://www.indeed.com/jobs?q=data+scientist&l=Sacramento%2C+CA&radius=100", 680, "data scientist")