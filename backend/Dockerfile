FROM python:3.9
RUN mkdir /app
WORKDIR /app/
ADD ./project /app/
COPY . .
RUN pip3 install -r requirements.txt
CMD ["python3", "-m","project"]