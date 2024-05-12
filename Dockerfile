FROM python:3.11

RUN mkdir /SHIFT_app

WORKDIR /SHIFT_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh