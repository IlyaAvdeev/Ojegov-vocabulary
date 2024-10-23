import re

class my_alg:
    def __init__(self):
        pass

    def find_special_words(filename):
        """
        Находит слова в файле, в которых три последние буквы повторяют три первые.

        Args:
          filename: Имя файла словаря (.txt).

        Returns:
          Список слов, удовлетворяющих условию.
        """
        special_words = []

        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                # Извлекаем слова, состоящие только из кириллических букв
                match = re.search(r'^\b([а-яА-Я]+)\b', line)
                if match:
                    word = match.group(1).lower()
                    if len(word) >= 6 and word[:3] == word[-3:]:
                        special_words.append(word)

        return special_words

if __name__ == '__main__':
    filename = "Ожегов С. Толковый словарь русского языка .txt"
    special_words = my_alg.find_special_words(filename)
    if special_words:
        print("Найдены следующие слова:")
        for word in special_words:
            print(word)
    else:
        print("Не найдено слов, удовлетворяющих условию.")