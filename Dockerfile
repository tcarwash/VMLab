FROM python:3.7

COPY ./ app/

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

ENV FLASK_APP=vmlab.py

EXPOSE 5000

ENTRYPOINT [ "./boot.sh" ]
