FROM dorowu/ubuntu-desktop-lxde-vnc:bionic

RUN mkdir -p /home/ubuntu/Desktop
RUN apt-get update && apt-get install -y python-pip wget actiona
RUN pip install selenium
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.25.0/geckodriver-v0.25.0-linux64.tar.gz
RUN tar xzf geckodriver-v0.25.0-linux64.tar.gz
RUN sudo mv geckodriver /usr/bin/geckodriver 
