FROM docker:dind

RUN apk add --no-cache \
    python3 \
    py3-pip \
    tzdata

ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
    


RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY . /app

WORKDIR /app

RUN pip3 install --no-cache-dir -r requirements.txt

RUN chmod +x /app/entry-point.sh
ENTRYPOINT ["/app/entry-point.sh"]

