FROM python:3.9.5-slim

WORKDIR /src/app
COPY requirements.txt /src/app/requirements.txt
RUN pip install -r requirements.txt
COPY . /src/app

RUN groupadd -r flask && useradd -r -g flask flask && \
    chown -R flask:flask /src

USER flask 

ENV FLASK_APP=PersonalBlog FLASK_RUN_HOST=0.0.0.0 DATABASE_URL=mysql+pymysql://root:root@db/main

EXPOSE 5000

CMD ["flask", "run"]