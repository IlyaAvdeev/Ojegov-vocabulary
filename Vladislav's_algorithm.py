import re
class vladislav_algorithm:
    def __init__(self):
        pass

    def find_special_words(filename):
        """
        Находит слова в файле, в которых три последние буквы повторяют три первые.

        Args:
          filename: Имя файла словаря (.txt).
        """

        # 1. Открываем файл для чтения
        with open(filename, 'r', encoding='utf-8') as file:
            # 1.1. Создаем множество для слов
            words_set = set()

            # 1.2. Читаем файл построчно
            for line in file:
                # 1.3. Разбиваем текст на отдельные слова
                words = re.findall(r'\b\w+\b', line)  # используем регулярное выражение для поиска слов
                # 1.4. Записываем слова в множество
                for word in words:
                    words_set.add(word.lower())  # добавляем слова в нижнем регистре

        # 2. Обработка каждого слова
        special_words_found = False
        for word in words_set:
            # 2.2. Проверить, что длина слова не меньше 6 символов
            if len(word) >= 6:
                # 2.3. Извлечь три первых и три последних символа слова
                first_three = word[:3]
                last_three = word[-3:]

                # 2.4. Сравнить извлеченные части
                if first_three == last_three:
                    print(word)
                    special_words_found = True

        if not special_words_found:
            print("Не найдено слов, удовлетворяющих условию.")

if __name__ == "__main__":
    filename = "Ожегов С. Толковый словарь русского языка .txt"
    vladislav_algorithm.find_special_words(filename)
