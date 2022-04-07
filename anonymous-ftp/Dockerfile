FROM python:3.6.5
RUN mkdir /usr/src/app

WORKDIR /usr/src/app

ADD requirements.txt /usr/src/app
RUN pip install -r requirements.txt
ADD . /usr/src/app

ENTRYPOINT ["/bin/bash", "-c"]
CMD ["/usr/src/app/entrypoint.py"]
