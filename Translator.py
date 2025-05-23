import csv
import sys
import os

def lineStartsWithCapitalLetter(line) -> bool:
    alphabet = list("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ")
    if line[0] in alphabet:
        return True
    return False



def dropEmptyLines(fw, pathToFile, sourceEncoding) -> None:
    with open(pathToFile, 'rt', encoding=sourceEncoding) as fr:
        for line in fr:
            if len(line.strip()) > 0:
                fw.write(line)

def concatLines(fw, pathToFile, sourceEncoding) -> None:
    with open(pathToFile, 'rt', encoding=sourceEncoding) as fr:
        while True:
            line1 = fr.readline()
            if len(line1) == 0:
                break
            extraLineExists = True
            while extraLineExists:
                extraLine = fr.readline()
                if len(extraLine) == 0:
                    fw.write(line1)
                    break
                if lineStartsWithCapitalLetter(extraLine):
                    fw.write(line1)
                    line1 = extraLine
                    extraLineExists = False
                else:
                    if line1.find("\r\n"):
                        line1 = line1.replace("\r\n", " ") + extraLine
                    else:
                        line1 = line1.replace("\n", " ") + extraLine
                    extraLineExists = True

def runner() -> None:
    workdir = os.environ.get('WORKDIR_PATH')
    outputdir = os.environ.get('OUTPPUTDIR_PATH')
    with open(outputdir + '/compressed_vocabulary.txt', 'w', newline='') as fw:
        dropEmptyLines(fw, workdir + '/Ожегов_С._Толковый_словарь_русского_языка.txt', 'utf-8')
    fw.close()

    with open(outputdir + '/each_word_on_its_line_vocabulary.txt', 'w', newline='') as fw:
        concatLines(fw, outputdir + '/compressed_vocabulary.txt', 'utf-8')
    fw.close()
    
if __name__ == '__main__':
    runner()