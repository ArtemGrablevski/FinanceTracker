FROM python:3.11

RUN mkdir /finance_tracker

WORKDIR /finance_tracker

COPY . .

RUN pip install -r requirements.txt

CMD [ "chmod", "a+x", "entrypoint.sh" ]
