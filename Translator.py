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

def replaceSimilarLetters(fw, pathToFile, sourceEncoding) -> None:
    with open(pathToFile, 'rt', encoding=sourceEncoding) as fr:
        for line in fr:
            newLine = line.replace("Ь1", "Ы").replace("O", "О").replace("X", "Х").replace("P", "Р").replace("B", "В").replace("Y","У").replace("H", "Н").replace("A", "А").replace("C", "С").replace("E", "Е").replace("K", "К").replace("M", "М").replace("T", "Т")
            fw.write(newLine)

def concatLines(fw, pathToFile, sourceEncoding) -> None:
    with open(pathToFile, 'rt', encoding=sourceEncoding) as fr:
        line1 = fr.readline()
        if len(line1) == 0:
            return
        extraLineExists = True
        while extraLineExists:
            extraLine = fr.readline()
            if len(extraLine) == 0:
                fw.write(line1)
                break
            if lineStartsWithCapitalLetter(extraLine):
                fw.write(line1)
                line1 = extraLine
                extraLineExists = True
            else:
                if line1.find("\r\n") != -1:
                    line1 = line1.replace("\r\n", " ") + extraLine
                else:
                    line1 = line1.replace("\n", " ") + extraLine
                extraLineExists = True

def extractHiddenWords(fw, pathToFile, sourceEncoding) -> None:
    with open(pathToFile, 'rt', encoding=sourceEncoding) as fr:
        for line in fr:
            if len(line.strip()) == 0:
                fw.write(line)
            elif lineStartsWithCapitalLetter(line.strip()):
                fw.write(line)
            else:
                wordsInLine = line.split(" ")
                newWordFound = False
                for word in wordsInLine:
                    if word.isupper():
                        if len(word) > 2:
                            index = line.find(word)
                            fw.write(line[:index])
                            fw.write("\n")
                            fw.write(line[index:])
                            print(line)
                            print("Extracted: " + line[index:])
                            newWordFound = True
                            break
                if newWordFound == False:
                    fw.write(line)



def runner() -> None:
    workdir = os.environ.get('WORKDIR_PATH')
    outputdir = os.environ.get('OUTPPUTDIR_PATH')

    with open(outputdir + '/letters_replaced.txt', 'w', newline='') as fw:
        replaceSimilarLetters(fw, workdir + '/Ожегов_С._Толковый_словарь_русского_языка.txt', 'utf-8')
    fw.close()

    with open(outputdir + '/extracted_hidden_words_vocabulary.txt', 'w', newline='') as fw:
        extractHiddenWords(fw, outputdir + '/letters_replaced.txt', 'utf-8')
    fw.close()

    with open(outputdir + '/compressed_vocabulary.txt', 'w', newline='') as fw:
        dropEmptyLines(fw, outputdir + '/extracted_hidden_words_vocabulary.txt', 'utf-8')
    fw.close()

    with open(outputdir + '/each_word_on_its_line_vocabulary.txt', 'w', newline='') as fw:
        concatLines(fw, outputdir + '/compressed_vocabulary.txt', 'utf-8')
    fw.close()

if __name__ == '__main__':
    runner()