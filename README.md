# PythonFlaskStatsDMySQLApp
StatsD Integration with Python Flask Mysql Application

The Dockerfile uses the base image from docker hub 'siddheshwarmore/pyapp-statsd'. This image includes the below things -

1. python setup
2. mysql server running with username=root, password=fr3sca
3. It deploys the flask app on the container on 5200 port.
4. you can browse the app on http://localhost:5200
5. python statsd client lib refer- https://statsd.readthedocs.io/en/v3.2.1/index.html#

How to deploy the docker image 

1. update the Dockerfile to use the correct ENV STATSD_SERVER="" and ENV STATSD_SERVER_PORT=8125
2. build the docker image - $ docker build -t flaskapp .
3. run docker container - $ docker run -d -p 5002:5002 flaskapp:latest

How to check the stats on graphite-

1. browse the app on http://localhost:5200 - refresh the page n times- this will incr the 'homepage' counter and sends the stats to graphite
2. Click on the 'Sign Up Today' butto  or hit http://localhos:5002/showSignUp - wait for pageload. do this for n time to get the graphs for timers 'ShowSignupTime' ang 'showSignUpt' gauges
