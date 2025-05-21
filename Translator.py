import csv
import sys

def transformToCSV(pathToFile, outputFolder, sourceEncoding) -> None:
    with open(outputFolder + '/output.csv', 'w', newline='') as fw:
        writer = csv.writer(fw)
    with open(pathToFile, 'rt', encoding=sourceEncoding) as fr:
        for line in fr:
            writer.writerow(line)

def runner() -> None:
    transformToCSV('/usr/src/app/Ожегов_С._Толковый_словарь_русского_языка.txt', '/output', 'utf-8')

if __name__ == '__main__':
    runner()