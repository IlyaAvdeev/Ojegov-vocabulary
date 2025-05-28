FROM python:3.13.3-alpine

ARG WORKDIR_NAME_ARG
ARG OUTPUTDIR_NAME_ARG

ENV WORKDIR_PATH=${WORKDIR_NAME_ARG}
ENV OUTPPUTDIR_PATH=${OUTPUTDIR_NAME_ARG}

WORKDIR ${WORKDIR_NAME_ARG}
RUN mkdir ${OUTPUTDIR_NAME_ARG}
COPY ./resources/requirements.txt ./
COPY ./resources/Ожегов_С._Толковый_словарь_русского_языка.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./TextProcessor.py" ]
