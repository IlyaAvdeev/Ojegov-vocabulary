
def transformToCSV(pathToFile, sourceEncoding):
    with open(pathToFile, 'rt', encoding=sourceEncoding) as f:
        for line in f:
            print(line)
    return content

def runner():
    transformToCSV('./Ожегов_С._Толковый_словарь_русского_языка.txt', 'utf-8')