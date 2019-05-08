# Use an official Python runtime as a parent image
FROM python:3.7-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt /app/pi/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r pi/requirements.txt
RUN pip install --upgrade requests

# Define environment variable
ENV NAME World

RUN apt-get update -y

#RUN apt-get install iceweasel -y
RUN apt-get install wget -y
RUN apt-get install curl -y
RUN apt-get install xvfb -y
RUN apt-get install bzip2 -y
RUN apt-get install iceweasel -y

RUN GECKODRIVER_VERSION=`curl https://github.com/mozilla/geckodriver/releases/latest | grep -Po 'v[0-9]+.[0-9]+.[0-9]+'` && \
    wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    tar -zxf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz

#RUN FIREFOX_SETUP=firefox-setup.tar.bz2 && \
 #   apt-get purge firefox && \
  ##  wget -O $FIREFOX_SETUP "https://download.mozilla.org/?product=firefox-latest&os=linux64" && \
  #  tar xjf $FIREFOX_SETUP -C /opt/ && \
  #  ln -s /opt/firefox/firefox /usr/bin/firefox && \
#rm $FIREFOX_SETUP

RUN geckodriver --version
RUN iceweasel --version

#RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz && \ 
#tar -xvzf geckodriver* && \ 
#chmod +x geckodriver && \ 
#mv geckodriver /usr/local/bin/ 

# Run app.py when the container launches
CMD ["python", "-u" ,"main.py"]
