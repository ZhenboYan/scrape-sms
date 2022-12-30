# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from time import sleep
import time
import requests
from datetime import datetime
import re 

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
phone_number = str(os.environ['PHONE_NUMBER'])
twilio_number = str(os.environ['TWILIO_NUMBER'])
http_website_url = str(os.environ['HTTP_WEBSITE_URL'])
low_alert = int(os.environ['LOW_ALERT']) + 1
scrape_rate = int(os.environ['SCRAPE_RATE'])
message = str(os.environ['MESSAGE'])

message = "From Lemonade: ~Meow~ My food is running low... meow hunggie"

client = Client(account_sid, auth_token)
old_text = ""
logic_acc = False
fed_state = True

while(1):
    if fed_state:
        print("detecting weight state")
        print(str(datetime.today().date()))
        old_day = str(datetime.today().date())
        get_site = requests.get(http_website_url)
        plain_text = get_site.text
        sentences = plain_text.split("\"}")
        
        if old_text != plain_text:
            for sentence in sentences:
                if sentence.find(str(datetime.today().date())) != -1: # found today's day
                    for i in range(low_alert):
                        find_sen = f"\"Food_Weight\":{i},\"Time\":\"{str(datetime.today().date())}"
                        if (sentence.find(find_sen) != -1 and sentence.find("Turn On") == -1):#don't send when just turn on
                            logic_acc = True
                
            if logic_acc:
                message = client.messages \
                    .create(
                        body=f'{message}',
                        from_=f'{twilio_number}',
                        to=f'+1{phone_number}'
                    )
                    
                print("weight below low alert")    
                print(message.sid)
                print("a message is sent!")
                fed_state = False
                logic_acc = False
        
        old_text = plain_text
    
    else:
        print("hungry state")
        print(str(datetime.today().date()))
        if str(datetime.today().date()) != old_day:
            fed_state = True
            
    sleep(scrape_rate)
