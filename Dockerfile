FROM python:latest

RUN pip3 install twilio
RUN wget -O /home/scrape_send_sms.py  https://raw.githubusercontent.com/ZhenboYan/scrape-sms/main/scrape_send_sms.py

ENTRYPOINT [ "python3","/home/scrape_send_sms.py" ]