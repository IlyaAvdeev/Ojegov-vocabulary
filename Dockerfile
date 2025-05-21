FROM python:3.13.3-alpine

WORKDIR /usr/src/app
RUN mkdir /output
COPY ./resources/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./Translator.py" ]
