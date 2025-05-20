FROM python:3

WORKDIR /usr/src/app

COPY ./resources/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./Translator.py" ]
