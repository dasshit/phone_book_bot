from enum import Enum


class BotTextEnum(str, Enum):
    """
    Текст для сообщений бота
    """
    WELCOME_TEXT = """Привет, это бот-телефонная книга
Я могу хранить и показывать контакты.
Пожалуйста, выберите, что вы хотите сделать:"""
    ENTER_CONTACT = """Отлично!
Теперь необходимо выбрать форму ввода контакта"""
    CHOOSE_OUTPUT_FORMAT = """Отлично!
Пожалуйста, выберете нужный формат вывода"""
    ENTER_NUMBER_TO_DELETE_CONTACT = """Отлично
Пожалуйста, введите номер телефона контакта, который хотите удалить"""
    ADD_CONTACT_SUCCESS = "Контакт успешно записан"
    INPUT_ERROR = "Ошибка ввода, попробуйте еще раз"
    ENTER_CONTACT_DATA = "Введите имя, фамилию или номер контакта"
    ENTER_CONTACT_NAME = """Пожалуйста, введите фамилию и имя контакта
Например: Пупкин, Василий"""
    COMMIN_BACK = "Идем назад"
    MULTI_LINE_CONTACT = """Фамилия: {}
Имя: {}
Номер: {}
Тип контакта: {}"""
    AFTER_SUCCESS_DELETE = "Контакт успешно удален"
    AFTER_FAILED_DELETE = "Контакт не найден"
    ERROR_TEXT = "Ошибка: {}"
    CONTACT_NOT_FOUND = "Контакт не найден"
    FILE_ERROR_TEXT = """Ошибка: 
Файл пока не существует, сохраните хотя бы один контакт"""


class UserTextCommandsEnum(str, Enum):
    """
    Текст из сообщений клавиатуры пользователя
    """
    PLACEHOLDER = "Выберите действие"
    WRITE_CONTACT = "Записать контакт"
    WRITE_CONTACT_BY_CARD = "Загрузить контакт из книги телефона"
    WRITE_CONTACT_BY_PARTS = "Ввести контакт поэтапно"
    SHOW_CONTACT = "Посмотреть контакт"
    SHOW_CONTACT_VCARD = "Показать контакт карточкой"
    SHOW_CONTACT_MULTI_LINE = "Показать контакт в несколько строк"
    SHOW_CONTACT_FILE = "Показать файл"
    DELETE_CONTACT = "Удалить контакт"
    BACK = "Назад"
