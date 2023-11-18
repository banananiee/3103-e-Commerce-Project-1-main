# This is for creationist purposes, especially in the event the image is gone

# Docker Image: morphocraft-django:1.1

# Grab python 3.11 container
FROM python:3.11

# Python set-up. Debate if the requirements should be done in pipefile instead especially to test for version dependencies
# COPY requirements.txt requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt
# RUN rm requirements.txt

# Java set-up for OWASP Check-Dependency
RUN apt update
RUN apt install -y openjdk-17-jdk
RUN mkdir /opt/java
RUN ln -s /usr/lib/jvm/java-17-openjdk-amd64 /opt/java/openjdk