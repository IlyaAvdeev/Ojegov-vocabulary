import os

def lineStartsWithCapitalLetter(line) -> bool:
    alphabet = list("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ")
    if line[0] in alphabet:
        return True
    return False

# Checks whether line begins with capitalized russian word or not.
def lineStartsWithCapitalizedWord(line) -> bool:
    wordsInLine = line.split(" ")
    word = wordsInLine[0]
    if word.isupper():
        if len(word) > 2:
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
            newLine = line.replace("...", "…").replace("O", "О").replace("X", "Х").replace("P", "Р").replace("B", "В").replace("Y","У").replace("H", "Н").replace("A", "А").replace("C", "С").replace("E", "Е").replace("K", "К").replace("M", "М").replace("T", "Т")
            fw.write(newLine)

"""
Пропускаем первые skipLines строк и 
объединяем все соседние строки в одну если последующие строки относятся к слову из первой строки. 
В итоге должны получить документ в котором в начале строки находится трактуемое слово
"""
def concatLines(fw, skipLines, pathToFile, sourceEncoding) -> None:
    with open(pathToFile, 'rt', encoding=sourceEncoding) as fr:
        for i in range(0,skipLines):
            fw.write(fr.readline())

        currentLetter = ''
        for line in fr:
            # --- предварительные проверки главной строки
            strippedLine = line.strip()
            #print("---Stripped line:" + strippedLine)
            if len(strippedLine) == 1: # в этом случае это переключение на новую букву
                currentLetter = strippedLine[0]
                # print("New letter:" + currentLetter, strippedLine)
                continue
            elif len(strippedLine) == 0: # значит файл закончился
                #print("!!!!End of file")
                return

            checkFollowingLines = True
            while checkFollowingLines:
                # --- предварительные проверки последующих строк которые в том числе потенциально могут быть частью главной строки
                nextLine = fr.readline()
                strippedNextLine = nextLine.strip()
                #print("Stripped next line:" + strippedNextLine)
                if len(strippedNextLine) == 0: #значит документ закончился и строк более нет
                    #print("!!!!End of file inside next line")
                    fw.write(strippedLine)
                    return
                if len(strippedNextLine) == 1: #значит начинается новая буква
                    currentLetter = strippedNextLine[0]
                    fw.write(strippedLine)
                    fw.write('\n')
                    # print("Новая буква в next line:", currentLetter, strippedLine)
                    break

                # ---------------------------------------------------------------------------------
                # --- с этого момента обрабатываем обычную строку (НЕ новая буква, НЕ конец файла)
                # ---------------------------------------------------------------------------------
                if strippedNextLine[0] != currentLetter[0]: # следующая считанная строка отличается от текущей буквы по которой обрабатываем
                    #print("Первые буквы неравны:", strippedNextLine, currentLetter)
                    if strippedLine.find("\r\n") != -1:
                        strippedLine = strippedLine.replace("\r\n", " ") + strippedNextLine
                    else:
                        strippedLine = strippedLine.replace("\n", " ") + strippedNextLine
                else:
                    #print("Первые буквы равны:", strippedNextLine, strippedLine)
                    fw.write(strippedLine)
                    fw.write('\n')
                    strippedLine = strippedNextLine
                    checkFollowingLines = True

def findInconsistencies(pathToFile, sourceEncoding) -> None:
    with open(pathToFile, 'rt', encoding=sourceEncoding) as fr:
        counter = 0
        for line in fr:
            if len(line) < 20:
                if line.find("см.") == -1:
                    print('"'+extractFirstWordFromLine(line)+'",    '+line)
                    counter = counter + 1
        print("Total:", counter)


"""
Разбирает каждую строку по словам и проверяем нет ли в строке слов в верхнем регистре длиной более 2 символов.
Если есть, то расчленяет исходную строку на несколько.
"""
def extractInlinedWords(fw, pathToFile, sourceEncoding) -> None:
    with open(pathToFile, 'rt', encoding=sourceEncoding) as fr:
        for line in fr:
            firstWord = extractFirstWordFromLine(line)
            wordsInLine = line.strip().split(" ")
            for word in wordsInLine:
                clearedWord = extractWordFromString(word)
                if clearedWord.isupper():
                    if firstWord in ("АББРЕВИАТУРА", "АВСТРОАЗИАТСКИЙ", "АВТОМАТИЗИРОВАТЬ", "АЖ", "АЙ", "АМЕРИКАНСКИЙ", "АНТИСОВЕТИЗМ",
                                     "АПАЧИ", "АССИРИЙЦЫ", "АССОРТИМЕНТ", "БАКС", "БАЮ-БАЙ", "БАЯДЕРА", "БЕЙ", "БЕЛО…", "БЕРЁСТА", "БЫЧАЧИЙ",
                                     "ЭПИЛЕПСИЯ", "ЭЛЕКТРОННО-ВЫЧИСЛИТЕЛЬНЫЙ", "ЭГЕ", "ЭНПИКЛОПЕДИЧНЫЙ", "ЭЗОПОВСКИЙ", "ЯРКО…", "СЕНАТ", "БАЙ",
                        "АНГЛО…", "АПОПЛЕКСИЯ", "БАЗИЛИКА", "БАРХАТКА", "ЯРЫГА", "ЯХТ…", "ЯЗЫКОЗНАНИЕ", "ЯГОДИЦА", "ШКВОРЕНЬ", "ШИЛОХВОСТЬ",
                        "ШВОРЕНЬ", "ЧТОБ", "ЧИСТО-…", "ЧИК-ЧИРИК", "ЧИНАРА", "ЧЕРНОБЫЛЬНИК", "ЧЕРНО…", "ЧЕРВИ", "ЧЕЛОВЕКО…", "ЧАРДАШ",
                        "ЦИДУЛЬКА", "ЦЕРКОВНО…", "ХО-ХО", "ХИ-ХИ", "ХИБАРА", "ХЕ-ХЕ", "ХВОРЬ", "ХАОС", "ХАНЖЕСТВО", "ХА-ХА", "ХАЛЯВА", "ХАЛДА",
                        "ФЬОРД", "ФРАНКО…", "ФЛАНЕЛЕВКА", "ФЛАГ…", "ФИЗИКА", "ФИГА", "УШКО", "УТРАМБОВАТЬ", "УРИЛЬНИК", "УПЛАТА", "УКСУСНИК", "УЖЕЛИ",
                        "УДЭХЭ", "УДАЛЬ", "УДАЛОЙ", "УГОН", "УГОЖДАТЬ", "УВОД", "УБОРКА", "УАЗИК", "ТЮНИК", "УТРАМБОВАТЬ","УСАДИТЬ","ТУТОВНИК","УТРАМБОВАТЬ",
                                     "ТОННЕЛЬ","ТРУТНИК","ТРЁШНИЦА","ТРЁШКА","ТРАПЕЗА","ТОТЧАС","ТОРЦЕВОЙ","ТОРФЯНИК","ТОРЕАДОР","ТОЖДЕСТВО","ТОВАРО…","ТЁША",
                                     "ТЕМНО…","ТЕЛЬНИК","ТВОРОГ","ТАРАТОРА","ТАНДЕМ","ТАБУРЕТ","СЫРОМЯТЬ","СЫЗМАЛА","СЧЁТНО…","СХАЛТУРИТЬ","СУ","СУРДИНА",
                                     "СУПОРОСАЯ","СТЮАРД","СТУДЕНИ","СТРОГАЛЬ","СТРИГУН","СТОРИЦЕЙ","СТОГОВАНИЕ","СТЕРНЯ","СТЕБЛИ","СТАНОВИЩЕ",
                                     "СТАЙКА","СРЫВ","СПЬЯНА","СПРОСОНОК","СПОЗАРАНКУ","СПЕРВОНАЧАЛА","СПАЗМ","СОУСНИК","СОСЛЕПА","СОРТАМЕНТ",
                                     "СОМО","СМЫ","ТУТА","ТУННЕЛЬ","СЫЗМАЛА","СЫРОМЯТЬ","СУПОРОСАЯ","СТОРИЦЕЙ","СТАНОВИЩЕ",
                                     "СРЫВ","СПЬЯНА","СОСЛЕПА","СОРТАМЕНТ","СМЁТКА","СМЕСИТЬ","СЛЫШЬ","СЛАЗИТЬ","СЛАБО…","СКАРЕД","СИММЕТРИЯ",
                                     "СИДМЯ","СИВКО","СЕЛИЩЕ","СГОН","СВОЗ","СВИТА","СВИНУХА","СВЕТОВОД","СВЕТЛЯК","САРДИНА","САМОСЕЙ","САЛЬТО",
                                     "САЛАТНИК","САЙГАК","САДНИТЬ","СВЕТЛО…","РЮШ","РЭКЕТИР","РЫБОНАДЗОР","РЭКЕТ","РЫБАРЬ","РУГНЯ","МАФИОЗИ",
                                     "РЭКЕТ", "РОЗАНЧИК","ПРОФЕССИОНАЛЬНО-ТЕХНИЧЕСКИЙ","ПСАЛТЫРЬ","ПУРПУРНО-…","РАЗВИЛКА","РАЗЖИМНОЙ","ПРОМЫСЛ",
                                     "ПРОСАДКА","ПРОСЫП","ПРОПОЛИС","ПРИПАЛИВАТЬ","ПРИСЫЛАТЬ","ПРОСЕКА","РАЗВОЗКА","ПРИНОС","РОЗГОВЕНЬЕ","РОЖЕНИЦА",
                                     "РАЗЪЁМ","ПРИКОРМ","РАКУРС","РАКУШЕЧНИК","РОВНЯ","РОГАЛИК","РЕФЕРИ","ПРИЖИВАЛ","ПРИЕЗД","ПРИГОН","ПРИВОД","РАСФАСОВАТЬ",
                                     "РАСПЛАНИРОВАТЬ","ПРЕДПЛЮСНА","ПРАДЕД","ПОЧИНИТЬ","ПОТОПИТЬ","ПОТЕМНЕНИЕ","ПОСТИЧЬ","ПОСЛУШНИК","ПОСКРЁБКИ","ПОЛИ"

                                     ):
                        fw.write(word)
                        fw.write(" ")
                        continue
                    if len(clearedWord) > 2:
                        fw.write("\n")
                        fw.write(clearedWord)
                        fw.write(", ")
                    else:
                        fw.write(word)
                        fw.write(" ")
                else:
                    fw.write(word)
                    fw.write(" ")
            fw.write("\n")



def extractFirstWordFromLine(line):
    if len(line) == 0:
        return ""
    wordsInLine = line.strip().split(" ")
    firstWord = extractWordFromString(wordsInLine[0])
    return firstWord

def extractWordFromString(str):
    if len(str) == 0:
        return ""
    extractedWord = str.lstrip().rstrip(",:.123456789!")
    return extractedWord

def runner() -> None:
    workdir = os.environ.get('WORKDIR_PATH')
    outputdir = os.environ.get('OUTPPUTDIR_PATH')

    # 1. Заменяем все русские символы которые распознались как латиница на русские схожие по написанию.
    with open(outputdir + '/01.letters_replaced.txt', 'w', newline='') as fw:
        replaceSimilarLetters(fw, workdir + '/Ожегов_С._Толковый_словарь_русского_языка.txt', 'utf-8')
    fw.close()

    # 2. Просмотриваем каждую строку на предмет наличия в ней других слов
    with open(outputdir + '/02.extracted_hidden_words_vocabulary.txt', 'w', newline='') as fw:
        extractInlinedWords(fw, outputdir + '/01.letters_replaced.txt', 'utf-8')
    fw.close()

    # 3. Вычищаем из файла все пустые строки
    with open(outputdir + '/03.compressed_vocabulary.txt', 'w', newline='') as fw:
        dropEmptyLines(fw, outputdir + '/02.extracted_hidden_words_vocabulary.txt', 'utf-8')
    fw.close()

    # 4. Слепить вместе строки которые жизнь разбросала по разным линиям
    with open(outputdir + '/04.concat_lines.txt', 'w', newline='') as fw:
        concatLines(fw, 4, outputdir + '/03.compressed_vocabulary.txt', 'utf-8')
    fw.close()

    # 5. Выводим подозрительные слова
    findInconsistencies(outputdir + '/04.concat_lines.txt', 'utf-8')

if __name__ == '__main__':
    runner()