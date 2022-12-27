from aiogram.fsm.context import FSMContext

from project.db.models import User


async def get_user_model(state: FSMContext) -> User:
    user_db_id = (await state.get_data()).get('USER_DB_ID')
    return User.get_by_id(user_db_id)
