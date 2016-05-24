# -*- coding: utf-8 -*-
"""
Created on Fri May 20 14:44:08 2016

@author: bikeshkawan
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import datetime

url = 'https://www.jobbnorge.no/en/available-jobs/research-development'
request = requests.get(url)
soup = BeautifulSoup(request.content,'lxml')

pagi_links = soup.findAll('div',{'class':'pagination'})

pagi_link_count=0
for a in soup.select('div.pagination a[href]'): # select all href inside div with class pagination
    pagi_link_count +=1
    
i = 1
total_jobs = 0
job_link = []
while i < (pagi_link_count+1):
    url = 'https://www.jobbnorge.no/en/available-jobs/research-development?page={}'.format(i)
    req = requests.get(url)
    soup = BeautifulSoup(req.content,'lxml')
    all_jobs = soup.findAll('span',{'itemprop':'title'})
    for jobs in all_jobs:
#         print(jobs.text)
        links =jobs.findAll('a')
        for link in links:
            job = "https://www.jobbnorge.no/{}".format(link['href'])
            job_link.append(job)
#             print(link['href'])
            total_jobs +=1
    i +=1
    
import smtplib
from email.header import Header
from email.utils import formataddr
def mail(TO,job,job_count):
    SUBJECT = "jobbnorge ({}) Jobs Expiring Soon Hurry UP!!".format(job_count)
    TEXT = "{}\n\n\n The End.....".format(job)
    # Gmail Sign In
    gmail_sender = 'sendermail@gmail.com'
    gmail_passwd = 'senderpassword'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)
    author = formataddr((str(Header(u'{} Jobs Expiring in a Week! HURRY UP !!'.format(job_count), 'utf-8')), "sendermail@gmail.com"))
    BODY = '\r\n'.join(['To: %s' % TO,'From: %s' % author,'Subject: %s' % SUBJECT,' ', TEXT])
    BODY = BODY.encode('ascii','ignore')
                        
                        

    try:
        server.sendmail(gmail_sender, [TO], BODY)
        print ('email sent')
    except:
        print("Seiding email failed")


    server.quit()
jobs = 'Below are List of jobs Expiring within 7 days\n----------------------------------------\n'
job_count = 0
i = 0
while i < len(job_link):
    url = job_link[i]
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'lxml')
    title = soup.findChildren('section')[0].findChildren('h2')[0]
   
    content = soup.findChildren('div',attrs={'class':'left-col col-3 info'})
 
    date = content[0].findChildren('div')[1].text
    employer = content[0].findChildren('div')[2].text
    municipality = content[0].findChildren('div')[3].text
    
    title = title.string.strip()
    employer = employer.strip()
    municipality = municipality.strip()
    date = date.replace("\r\n"," ")
    date = date.strip()
    
    today = datetime.date.today()
    deadlines = datetime.datetime.strptime(date, "%m/%d/%Y").date()
    difference = deadlines - today

    days_left = int(difference.days)
    
    
    
    if days_left == 7:
        jobs +="\n ********** 7 Days Left ************* \n\n  Job Title:   {} \n\n University:   {} \n\n Location:   {} \n DeadLine:   {}\n Job Link:   {}\n----------------------------------------\n\n".format(title,employer,municipality,date,url)
        print('[{}] :  True'.format(i+1))
        print("Days Left:", days_left)
        print(title)
        print(url)
        print("*****************************************")
        job_count +=1

    if days_left == 3:
        jobs +="\n ********** 3 Days Left ************* \n\n  Job Title:   {} \n\n University:   {} \n\n Location:   {} \n DeadLine:   {}\n Job Link:   {}\n----------------------------------------\n\n".format(title,employer,municipality,date,url)
        print('[{}] :  True'.format(i+1))
        print("Days Left:", days_left)
        print(title)
        print(url)
        print("*****************************************")
        job_count +=1


    if days_left == 1:
        
        jobs +="\n ********** 1 Day Left ************* \n\n  Job Title:   {} \n\n University:   {} \n\n Location:   {} \n DeadLine:   {}\n Job Link:   {}\n----------------------------------------\n\n".format(title,employer,municipality,date,url)
        print('[{}] :  True'.format(i+1))
        print("Days Left:", days_left)
        print(title)
        print(url)
        print("*****************************************")
        job_count +=1
        
    else:
        print('[{}] :  False'.format(i+1))
        print("Days Left: ", days_left ,"\n*************\n")
        
    i+=1
print("The End")
mail('bikeshkawang@gmail.com',jobs,job_count)





