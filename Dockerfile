FROM alpine:3.13.2
MAINTAINER Mumtaz Ahmad <mumtaz.ahmad@siemens.com>

ARG BRANCH=defaultValue
ARG COMMIT=defaultValue
ARG CODE_REPOSITORY=defaultValue

RUN echo "Building for $COMMIT"
RUN apk add --no-cache tzdata
RUN apk add --no-cache python3 py3-pip
RUN pip3 install --upgrade pip
RUN pip install termcolor
RUN apk add git
RUN mkdir -p /src
RUN git clone $CODE_REPOSITORY --depth=1 --branch $BRANCH --single-branch src
RUN git config --global --add safe.directory /app



