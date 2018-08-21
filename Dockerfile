FROM python:3.3-alpine
MAINTAINER Nealyip

RUN apk --no-cache add git && \
    git clone https://github.com/nealyip/facebook_oauth.git /app

EXPOSE 8080
WORKDIR /app

CMD ["/usr/local/bin/python", "index.py"]