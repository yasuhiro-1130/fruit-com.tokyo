FROM python:3.7-alpine  

WORKDIR /usr/src/fruits  

ENV PYTHONDONTWRITEBYTECODE 1  
ENV PYTHONUNBUFFERED 1  

# psycopg2のインストール  
RUN apk update \
	&& apk add --virtual build-deps gcc python3-dev musl-dev \
	&& apk add postgresql-dev \
	&& pip install psycopg2 \
	&& apk del build-deps \
# pillowインストールのため追加
	&& apk add --no-cache jpeg-dev zlib-dev

# pillowインストールのため追加
RUN apk add --no-cache --virtual .build-deps build-base linux-headers

RUN pip install --upgrade pip 

COPY ./requirements.txt /usr/src/fruits/requirements.txt 

RUN pip install -r requirements.txt

COPY fruits/ /usr/src/fruits/  

ENTRYPOINT ["sh", "/usr/src/fruits/entrypoint.sh"]