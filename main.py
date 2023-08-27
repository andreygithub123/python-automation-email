import requests # http requests

from bs4 import BeautifulSoup #web scraping

import smtplib #sending the email

#email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import datetime #system date and time manipulation

now=datetime.datetime.now()
content = ''


#extacting the news
def extracting_news(url):
    print('extracting the news ...')
    cnt = '' # used to fill content variable
    cnt +=('<b>Hot News:</b>\n' + '<br> '+ '-'*50+'</br') #50 making it more readble
    response=requests.get(url) #send an HTTP GET request to a specified URL and retrieve the content of the web page associated with that URL
    content_function=response.content #provides the raw binary content of the server's response to an HTTP request
    soup = BeautifulSoup(content_function,'html.parser') # gives you access to a lot of bs4 methods
    for i,tag in enumerate(soup.find_all('td',attrs={'class':'title','valing':''})):
        cnt+= ( (str(i+1)+' :: '+tag.text + "\n" + '<br') if tag.text!='More' else '')
    return(cnt)

cnt = extracting_news('https://news.ycombinator.com/')
content += cnt
content += ('<br>------<br>')
content += ('<br><br>End of Message')

#sending the email

#email details

SERVER = 'smtp.gmail.com'
PORT = 587
FROM = '*********'
TO = '*********'
PASS = '*********' # password

#msg creation

msg=MIMEMultipart()
msg['Subject'] = ' Top News From Python Generated ' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(now.year)
msg['From'] = FROM
msg['To']= TO

msg.attach(MIMEText(content,'html'))

print('Initating Server...')
server=smtplib.SMTP(SERVER,PORT)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(FROM,PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email sent...')

server.quit()