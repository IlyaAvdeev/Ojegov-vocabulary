import csv
import sys
import os

def dropEmptyLines(fw, pathToFile, sourceEncoding) -> None:
    with open(pathToFile, 'rt', encoding=sourceEncoding) as fr:
        for line in fr:
            if len(line.strip()) > 0:
                fw.write(line)
    
def runner() -> None:
    workdir = os.environ.get('WORKDIR_PATH')
    outputdir = os.environ.get('OUTPPUTDIR_PATH')
    with open(outputdir + '/compressed_vocabulary.txt', 'w', newline='') as fw:
        dropEmptyLines(workdir + '/Ожегов_С._Толковый_словарь_русского_языка.txt', outputdir, 'utf-8')
    fw.close()
    
if __name__ == '__main__':
    runner()