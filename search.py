# Поиск
# Для чтения файлов
import os

# Для добавления нескольких разделителей
import re

# Изменение директории
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

# Основной словарь
dictionary = {}
# Он устроен таким образом -
# {слово: [{номер файла1 : [позиция1, позиция2]}, {номер файла2 : [позиция1, поозиция2]},
# {номер файла4 : [позиция1]}]})
# Причем сохраняются словари только тех файлов, в которых слово присутствует
# (например тут пропущен номер файла3 - там слова нет)


# Массив текстовых файлов
textfiles = ["example1.txt", "example2.txt", "example3.txt"]

# Проход по массиву текстовых файлов
for i in range(len(textfiles)):
    with open(textfiles[i], "r", encoding="windows-1251") as file:
        # Рассмотрение файлов построчно
        word_position = 0
        for line in file:
            # А каждая строка рассматривается по словам
            # Разделение на слова разными разделителями
            s = [s for s in re.split(r"[.,\s;:-]+", line)]
            for word in s:
                word_position += 1
                k = word.lower()
                # Если слова еще нет в словаре, добавляем, само слово - ключ
                if k not in dictionary:
                    # По умолчанию для нового слова k - слово, i + 1 - номер файла, в котором слово встретилось первый раз
                    # Позиция в этом файле, на которой слово было обнаружено
                    dictionary.update({k: [{i + 1: [word_position]}]})
                else:
                    # Если слово уже есть в словаре

                    # Если в конкретном файле слова еще не было
                    # Смотрим последний элемент, для нового файла
                    if i + 1 not in dictionary[k][-1]:
                        # Добавляем словарь, где ключ - номер файла, а значение - пустой массив позиций
                        dictionary[k].append({i + 1: []})
                    # Если слово уже было в этом файле, добавляем в массив позиций новую позицию
                    dictionary[k][-1][i + 1].append(word_position)
            # print(k)
        # print()

# Вывод получившегося словаря
for key, value in dictionary.items():
    print(f"{key}: {value}")


def key_check(key):
    return key in dictionary


def and_request(word1, word2):
    if not (key_check(word1) and key_check(word2)):
        print("Одно или оба слова не содержатся в словаре")
        return

    answer = []
    # p1 и p2 массивы ключей для word1 и word2, то есть массивы номеров файлов, в которых есть эти слова
    p1 = [[*i][0] for i in dictionary[word1]]
    p2 = [[*i][0] for i in dictionary[word2]]
    # [*i] - распаковка словаря, список ключей. Но так как ключ у нас только один, список из одного элемента -> элемент
    # При помощи [*i][0]
    i = j = 0
    while i != len(p1) and j != len(p2):
        if p1[i] == p2[j]:
            answer.append(p1[i])
            i += 1
            j += 1
        elif p1[i] < p2[j]:
            i += 1
        else:
            j += 1
    return answer


def or_request(word1, word2):
    if not (key_check(word1) and key_check(word2)):
        print("Одно или оба слова не содержатся в словаре")
        return
    answer = []
    p1 = [[*i][0] for i in dictionary[word1]]
    p2 = [[*i][0] for i in dictionary[word2]]
    # Помещаем в ответ целиком p1, и p2, исключая пересечение
    answer = p1 + [i for i in p2 if i not in p1]
    answer.sort()
    return answer


# Проверка, содержится ли слово в словаре
def not_request(word1):
    if not key_check(word1):
        print("Слово не содержится в словаре")
        return
    p1 = [[*i][0] for i in dictionary[word1]]
    # all_mass - массив номеров всех файлов
    all_mass = list(range(1, len(textfiles) + 1))
    # В ответ помещаем те номера файлов, которых нет в p1
    return [i for i in all_mass if i not in p1]


# Функция для обработки строки
def parse_and_evaluate(expression):
    # В зависимости от того, какой оператор содержится в строке
    if " and " in expression or " и " in expression:
        # Разбиваем строку на части, аргументы, можно использовать and или и
        parts = re.split(r"\b(?:and|и)\b", expression, flags=re.UNICODE)
        # Если число аргументов верное
        if len(parts) == 2:
            arg1, arg2 = parts
            # Вызываем функцию and_request
            return and_request(arg1.strip(), arg2.strip())
        else:
            # Если введено неверное число аргументов
            print("Некорректное выражение. Должно быть два аргумента")
            return
    elif " or " in expression or " или " in expression:
        parts = re.split(r"\b(?:or|или)\b", expression, flags=re.UNICODE)
        if len(parts) == 2:
            arg1, arg2 = parts
            return or_request(arg1.strip(), arg2.strip())
        else:
            print("Некорректное выражение. Должно быть два аргумента")
            return
    elif "not " in expression or "без " in expression:
        parts = expression.split()

        if len(parts) == 2:
            arg = parts[1]
            return not_request(arg)
        else:
            print("Некорректное выражение. Должен быть один аргумент")
            return
    # Если в строке не оказалось ни одного оператора
    else:
        print("Некорректное выражение")
        return


print("\nВведите запрос для поиска по словарю. Для выхода из программы - введите end")
print("Доступны следующе запросы - and, or, not. И на русском языке - или, и, без\n")
request = input("Запрос: ").lower()
while request != "end":
    result = parse_and_evaluate(request)
    if (result != None) and (result != []):
        print(*[textfiles[i - 1] for i in result], sep=", ")
    else:
        print("Нет соответствующих запросу файлов")
    request = input("Запрос: ").lower()

print()
