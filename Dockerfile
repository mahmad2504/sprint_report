FROM alpine:3.13.2
MAINTAINER Mumtaz Ahmad <mumtaz.ahmad@siemens.com>
ARG COMMIT=defaultValue
ARG CODE_REPOSITORY=defaultValue

RUN echo "Building for $COMMIT"
RUN apk add --no-cache tzdata
RUN apk add --no-cache python3 py3-pip
RUN pip install termcolor
RUN apk add git
RUN mkdir -p /src
RUN git clone $CODE_REPOSITORY /src
WORKDIR /src
RUN git checkout $COMMIT
RUN ls

