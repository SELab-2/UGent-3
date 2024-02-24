FROM python:3.9
RUN mkdir /app
WORKDIR /app
ADD ./project /app/
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 5000
COPY . /app
ENTRYPOINT ["python3"]
CMD ["__main__.py"]