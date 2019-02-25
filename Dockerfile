FROM python:3.6.7

RUN apt-get update && apt-get -y install cron
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
ADD cron /etc/cron.d/interwebs-speed-test
RUN chmod 0644 /etc/cron.d/interwebs-speed-test
RUN crontab /etc/cron.d/interwebs-speed-test

CMD ["cron", "-f"]
