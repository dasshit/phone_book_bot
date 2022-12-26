import os.path
import typing

from aiogram.types import Contact


def get_phone_book_path(user_name: str) -> str:
    """
    Получение пути к файлу телефонной книги пользования user_name
    :param user_name: Имя пользователя
    :return: Путь к файлу телефонной книги
    """
    return os.path.join('contacts', f'phone_book_{user_name}.txt')


def handle_line(line: str) -> tuple[str, ...]:
    """
    Обработка строки с удалением лишних пробелов
    :param line: Строка с данными контакта
    :return: Результат обработки
    """
    items = tuple(item.strip() for item in line.split(','))
    return items


def handle_contact(contact: Contact, user_name: str):
    """
    Обработка контакта при получении его ввиде карточки
    :param contact: Контакт
    :param user_name: имя пользователя, приславшего сообщение
    """
    assert contact.phone_number, 'Контакт не имеет номера телефона'
    assert contact.first_name, 'Контакт не имеет имени'
    assert contact.last_name, 'Контакт не имеет фамилии'
    line = (contact.first_name, contact.last_name, contact.phone_number, 'phonebook')
    write_line(line=line, user_name=user_name)


def check_line(line: tuple[str, ...]) -> bool:
    """
    Проверка строки
    """
    assert len(line) == 4, 'Ошибка ввода, повторите попытку'


def checked_handle_line(line: str) -> tuple[str, ...]:
    """
    Обработка и проверка данных контакта
    """
    line = handle_line(line)
    check_line(line)
    return line


def write_line(line: tuple[str, ...], user_name: str):
    """
    Запись контакта в книгу
    :param line: данные контакта
    :param user_name: имя пользователя, приславшего сообщение
    """
    with open(get_phone_book_path(user_name), 'a') as f:
        f.write(','.join(line) + '\n')


def find_line(line: str, user_name: str) -> typing.Optional[tuple[str, ...]]:
    """
    Поиск контакта в книге
    :param line: Данные для поиска
    :param user_name: имя пользователя, приславшего сообщение
    :return: Найденный контакт
    """
    line = ','.join(handle_line(line))
    reversed_line = ','.join(handle_line(line)[::-1])

    with open(get_phone_book_path(user_name), 'r') as f:
        for f_line in f.readlines():
            if line in f_line or reversed_line in f_line:
                return handle_line(f_line)
        else:
            raise ValueError('Контакт не найден')


def delete_line(line: str, user_name: str):
    """
    Удаление контакта
    :param line: Данные для поиска
    :param user_name: имя пользователя, приславшего сообщение
    """
    line = ','.join(handle_line(line))
    reversed_line = ','.join(handle_line(line)[::-1])
    with open(get_phone_book_path(user_name), 'r') as f:
        lines = f.readlines()

    flag = False

    for i, f_line in enumerate(lines.copy()):
        if line in f_line or reversed_line in f_line:
            flag = True
            lines.pop(i)
            break

    assert flag, 'Контакт не найден, удаление не выполнено'

    if lines:
        with open(get_phone_book_path(user_name), 'w') as f:
            f.writelines(lines)
    else:
        os.remove(get_phone_book_path(user_name))

