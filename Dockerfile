FROM rockylinux:9.1.20221221
RUN yum install -y pip python3 wget
RUN pip3 install twilio requests
RUN wget -O /home/run.sh  https://raw.githubusercontent.com/ZhenboYan/scrape-sms/main/run.sh
RUN chmod +x /home/run.sh
ENTRYPOINT ["/home/run.sh" ]

# FROM alpine:latest
# RUN apk add --no-cache python3 py3-pip
# RUN apk install wget
# RUN pip3 install twilio
