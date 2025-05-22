import csv
import sys
import os

def transformToCSV(pathToFile, outputFolder, sourceEncoding) -> None:
    with open(outputFolder + '/output.csv', 'w', newline='') as fw:
        with open(pathToFile, 'rt', encoding=sourceEncoding) as fr:
            for line in fr:
                if len(line.strip()) > 0:
                    fw.write(line)
    fw.close()

def runner() -> None:
    workdir = os.environ.get('WORKDIR_NAME')
    outputdir = os.environ.get('OUTPUTDIR_NAME')
    transformToCSV(workdir + '/Ожегов_С._Толковый_словарь_русского_языка.txt', outputdir, 'utf-8')

if __name__ == '__main__':
    runner()