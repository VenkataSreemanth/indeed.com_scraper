BIA660 Final Project
indeed.com scraper and job type predictor

The first file to run is the web scraper. The scraper takes as input a URL to the first page of the job listings to a particular job and returns a csv of the text descriptions of each job, and the job type, spearated by comma.

The basic steps of the scraper are:
1. open the html containing the list of jobs
2. get the 'a' tag for each job from the list of jobs
3. open the url for each a tag (for each job).
4. save the html for the job site into disc
5. get the job text for each job_html and add it to a row in the csv

The lines on the scraper are extensively commented, so pleae open the file to see setailed info on what each line is doing.

To run, input the URL, the number of pages you'd like to examine (there are 15 jobs per page), and the job type (one of: data enginner, data scientist, software engineer)

for example: 
run_scraper("https://www.indeed.com/jobs?q=Data+Engineer&l=Washington%2C+DC&radius=100", 2, "data engineer")
will get the first 30 jobs for data engineer in washington DC