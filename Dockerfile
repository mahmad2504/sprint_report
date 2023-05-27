FROM alpine:3.13.2
MAINTAINER Mumtaz Ahmad <mumtaz.ahmad@siemens.com>

RUN apk add --no-cache tzdata
RUN apk add --no-cache python3 py3-pip
RUN pip install termcolor

RUN mkdir -p /src
COPY ./* /src/