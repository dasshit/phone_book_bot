import csv

from aiogram.fsm.context import FSMContext

from project.db.models import User, Contact


async def get_user_model(state: FSMContext) -> User:
    """
    Получение модели пользователя
    """
    user_db_id = (await state.get_data()).get('USER_DB_ID')
    return User.get_by_id(user_db_id)


def writeToCsv(data, filename):
    print("Writing to csv: {} ...".format(filename))
    with open(filename, 'w', newline='') as out:
        csvOut = csv.writer(out)
        # column headers
        headers = [x for x in Contact._meta.sorted_field_names]
        csvOut.writerow(headers)

        # write data rows
        for row in data:
            csvOut.writerow(row)
