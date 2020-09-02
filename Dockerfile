FROM dorowu/ubuntu-desktop-lxde-vnc:bionic

ENV DEBIAN_FRONTEND=noninteractive
ENV SCREEN_WIDTH=1920
ENV SCREEN_HEIGHT=1080
ENV SCREEN_DEPTH=24
ENV SCREEN_DPI=74

RUN mkdir -p /home/ubuntu/Desktop
RUN apt-get update && apt-get install -y python-pip wget actiona
RUN pip install selenium
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.25.0/geckodriver-v0.25.0-linux64.tar.gz
RUN tar xzf geckodriver-v0.25.0-linux64.tar.gz
RUN mv geckodriver /usr/bin/geckodriver 

WORKDIR /root/Desktop/
