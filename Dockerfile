FROM siddheshwarmore/pyapp-statsd:latest

RUN mkdir -p /app

WORKDIR /app

ADD . /app

# 
ENV DB_USER=root
ENV DB_PASS=fr3sca
ENV DB_NAME=BucketList
ENV DB_HOST=localhost
ENV STATSD_SERVER=172.31.10.134
ENV STATSD_SERVER_PORT=8125

EXPOSE 5002

#RUN nohup python app.py &

CMD ["python", "app.py"]

