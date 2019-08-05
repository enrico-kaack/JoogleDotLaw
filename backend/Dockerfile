FROM python:3

ADD . /

RUN pip install -r requirements.txt

RUN unzip urteile.zip 

RUN ls

RUN python setup.py

EXPOSE 5000

CMD [ "python", "server.py" ]

