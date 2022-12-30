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
send_message = str(os.environ['MESSAGE'])
my_number = str(os.environ['MY_NUMBER'])

client = Client(account_sid, auth_token)
prev_sen = ""
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
        
        sentence = sentences[-2]
        find_weight = sentence.split(",{\"Food_Weight\":")[1].split(",\"")
        weight = int(find_weight[0])
        print(weight)
        
        if prev_sen != sentence:
            if (weight <= low_alert and sentence.find("Turn On") == -1):#don't send when just turn on
                logic_acc = True
                send_message = send_message + f" Food is less than {weight}g now."
                
            if logic_acc:
                message = client.messages \
                    .create(
                        body=f'{send_message}',
                        from_=f'{twilio_number}',
                        to=f'+1{phone_number}'
                    )
                message2 = client.messages \
                    .create(
                        body=f'{send_message}',
                        from_=f'{twilio_number}',
                        to=f'+1{my_number}'
                    )

                print("weight below low alert")    
                print("a message is sent!")
                print(message.sid)
                fed_state = False
                logic_acc = False
        
        prev_sen = sentence

    else:
        print("hungry state")
        print(str(datetime.today().date()))
        if str(datetime.today().date()) != old_day:
            fed_state = True
            
    sleep(scrape_rate)
