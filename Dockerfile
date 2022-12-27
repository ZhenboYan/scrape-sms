FROM python3

RUN pip3 install twilio
RUN wget -O /home/scrape_send_sms.py https://raw.githubusercontent.com/zhenboyan/web_scrape_sms/main/scrape_send_sms.py
 
ENTRYPOINT [ "/home/scrape_send_sms.py" ]