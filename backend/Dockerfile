FROM docker:dind as builder

FROM python:3.9

COPY --from=builder /usr/local/bin/docker /usr/local/bin/docker

RUN mkdir /app
WORKDIR /app

ADD ./project /app/

COPY requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt

COPY . /app

CMD ["/app/entry-point.sh"]
#ENTRYPOINT ["python"]
#CMD ["__main__.py"]
