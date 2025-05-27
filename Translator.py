import os

# Checks whether line begins with capital russian letter or not.
def lineStartsWithCapitalLetter(line) -> bool:
    alphabet = list("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ")
    if line[0] in alphabet:
        return True
    return False

# Удаляем все строки котоыре после отсечения пробелов и табуляций превращаются в пустую строку
def dropEmptyLines(fw, pathToFile, sourceEncoding) -> None:
    with open(pathToFile, 'rt', encoding=sourceEncoding) as fr:
        for line in fr:
            if len(line.strip()) > 0:
                fw.write(line)

"""
заменяем все символы, которые распознались латиницей на русские буквы схожие по написанию.
здесь применяем только к буквам в верхнем регистре.
"""
def replaceSimilarLetters(fw, pathToFile, sourceEncoding) -> None:
    with open(pathToFile, 'rt', encoding=sourceEncoding) as fr:
        for line in fr:
            newLine = line.replace("Ь1", "Ы").replace("O", "О").replace("X", "Х").replace("P", "Р").replace("B", "В").replace("Y","У").replace("H", "Н").replace("A", "А").replace("C", "С").replace("E", "Е").replace("K", "К").replace("M", "М").replace("T", "Т")
            fw.write(newLine)

"""
объединяем все соседние строки в одну если последующие строки относятся к слову из первой строки. 
В итоге должны получить документ в котором в начале строки находится трактуемое слово, но может получиться так что в строке есть 
ещё другие трактуемые слова
"""
def concatLines(fw, pathToFile, sourceEncoding) -> None:
    with open(pathToFile, 'rt', encoding=sourceEncoding) as fr:
        extraLineExists = True
        while True:
            if extraLineExists:
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
                    extraLineExists = False
                else:
                    if line1.find("\r\n") != -1:
                        line1 = line1.replace("\r\n", " ") + extraLine
                    else:
                        line1 = line1.replace("\n", " ") + extraLine
                    extraLineExists = True

"""
Разбирает каждую строку по словам и проверяем нет ли в строке слов в верхнем регистре длиной более 2 символов.
Если есть, то расчленяет исходную строку на несколько.
"""
def extractHiddenWords(fw, pathToFile, sourceEncoding) -> None:
    with open(pathToFile, 'rt', encoding=sourceEncoding) as fr:
        for line in fr:
            wordsInLine = line.split(" ")
            for word in wordsInLine:
                if word.isupper():
                    if len(word) > 2:
                        if (word != "-СЯ"):
                            fw.write("\n")
                fw.write(word)
                fw.write(" ")


def runner() -> None:
    workdir = os.environ.get('WORKDIR_PATH')
    outputdir = os.environ.get('OUTPPUTDIR_PATH')

    # 1. Заменяем все русские символы которые распознались как латиница на русские схожие по написанию.
    with open(outputdir + '/letters_replaced.txt', 'w', newline='') as fw:
        replaceSimilarLetters(fw, workdir + '/Ожегов_С._Толковый_словарь_русского_языка.txt', 'utf-8')
    fw.close()

    # 2. Просмотриваем каждую строку на предмет наличия в ней других слов
    with open(outputdir + '/extracted_hidden_words_vocabulary.txt', 'w', newline='') as fw:
        extractHiddenWords(fw, outputdir + '/letters_replaced.txt', 'utf-8')
    fw.close()

    # 3. Вычищаем из файла все пустые строки
    with open(outputdir + '/compressed_vocabulary.txt', 'w', newline='') as fw:
        dropEmptyLines(fw, outputdir + '/extracted_hidden_words_vocabulary.txt', 'utf-8')
    fw.close()

    # 4. объединяем все строки относящиеся к одному слову в одну строку. В итоге каждую строку должно занимать своё слово
    with open(outputdir + '/each_word_on_its_line_vocabulary.txt', 'w', newline='') as fw:
        concatLines(fw, outputdir + '/compressed_vocabulary.txt', 'utf-8')
    fw.close()

if __name__ == '__main__':
    runner()