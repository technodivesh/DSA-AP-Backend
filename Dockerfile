# import the base image Debian:Bullseye:Python:3.8
FROM python:3.8
RUN pip install --upgrade pip
# set environment variables and terminal arguments
# ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# ARG DEBIAN_FRONTEND=noninteractive
# ARG ACCEPT_EULA=Y
# copy requirements and setting file to respective location
ARG DEBIAN_FRONTEND=noninteractive
ARG ACCEPT_EULA=Y
# update and install application dependency
RUN apt update\
    && apt-get install unixodbc unixodbc-dev -y\
    && apt-get clean -y
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -\
    && curl https://packages.microsoft.com/config/debian/10/prod.list\
    > /etc/apt/sources.list.d/mssql-release.list
RUN apt update\
    && apt-get install -y msodbcsql17
WORKDIR /app
ADD . /app
COPY ./requirements.txt /app/requirements.txt
# install python libraries from requirements.txt
RUN pip install -r requirements.txt
# copy application code
COPY . /app
# expose port to outer world and execute application
EXPOSE 8010
# 0.0.0.0:80 replace with azure URL for backend service
CMD ["python", "/app/src/manage.py", "runserver", "0.0.0.0:8010"]