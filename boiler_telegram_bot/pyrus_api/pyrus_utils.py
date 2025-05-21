from pprint import pprint
from typing import Dict

from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode

from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_states import BoilerDialog
from pyrus_api.pyrus_client import PyrusClient


def get_form_and_field_id_by_form_name(pyrus_forms_data: dict, form_name: str, fields_name: list):
    pyrus_id_data = {
    }
    for form_data in pyrus_forms_data.get('forms'):
        if form_data.get('name').lower() == form_name.lower():
            pyrus_id_data['form_id'] = form_data.get('id')
            form_field = form_data.get('fields')
            for field in form_field:
                if field.get('name').lower() in fields_name:
                    pyrus_id_data[field.get('name')] = field.get('id')
            return pyrus_id_data


def get_client_catalog_id(pyrus_catalog_data: dict):
    catalogs_data = pyrus_catalog_data.get('catalogs')
    catalogs_data: Dict
    for catalog in catalogs_data:
        if catalog.get('name') == 'Клиенты':
            return catalog.get('id')


async def send_form_task(callback: CallbackQuery, user_name: str, user_phone: str, task_title: str,
                         task_description: str, user_address: str, client: int, dialog_manager: DialogManager):
    await dialog_manager.switch_to(
        BoilerDialog.boiler_waiting_status
    )

    pyrus_forms_response = PyrusClient.request('GET', '/forms')
    if pyrus_forms_response.status_code == 200:
        forms_data = pyrus_forms_response.json()  # должен быть список
        pyrus_id_data = get_form_and_field_id_by_form_name(pyrus_forms_data=forms_data,
                                                           form_name='лиды с сайта',
                                                           fields_name=['проблема', 'описание', 'имя', 'телефон',
                                                                        'адрес', 'клиент'])

        pyrus_task_data = {
            'form_id': pyrus_id_data.get('form_id'),
            'fields': [
                {
                    'id': pyrus_id_data.get('Проблема'),
                    'value': task_title
                },
                {
                    'id': pyrus_id_data.get('Описание'),
                    'value': task_description
                },
                {
                    'id': pyrus_id_data.get('Имя'),
                    'value': user_name
                },
                {
                    'id': pyrus_id_data.get('Телефон'),
                    'value': user_phone
                },
                {
                    'id': pyrus_id_data.get('Адрес'),
                    'value': user_address
                },
                # {
                #     'id': pyrus_id_data.get('Клиент'),
                #     'value': {
                #         'item_id': client  # TODO добавить запрос на поиск клиента или его добавление (просто ID)
                #     }
                # },
            ]
        }

        pyrus_task_response = PyrusClient.request(
            method='POST', endpoint='/tasks', json=pyrus_task_data
        )

        if pyrus_task_response.status_code == 200:
            pyrus_task_data = pyrus_task_response.json()
            pyrus_task_id = pyrus_task_data['task']['id']

            await callback.message.answer(
                text="✅ <b>Заявка успешно принята!</b>\n\n"
                     f"Номер заявки: <b>{pyrus_task_id}</b>\n\n"
                     "📞 Ожидайте звонка.",
                parse_mode=ParseMode.HTML
            )

            dialog_manager.show_mode = ShowMode.DELETE_AND_SEND

            await dialog_manager.switch_to(
                BoilerDialog.boiler_main_menu
            )

        else:
            print(pyrus_task_response.status_code)
            print(pyrus_task_response.text)

            await callback.message.answer(
                text='⚠️ Упс! Кажется, что-то пошло не так.\n'
                     'Попробуйте позже.',
                parse_mode=ParseMode.HTML
            )

            dialog_manager.show_mode = ShowMode.DELETE_AND_SEND

            await dialog_manager.switch_to(
                BoilerDialog.boiler_main_menu
            )

    else:
        print(pyrus_forms_response.status_code)
        print(pyrus_forms_response.text)
        await callback.message.answer(
            text='⚠️ Упс! Кажется, что-то пошло не так.\n'
                 'Попробуйте позже.',
            parse_mode=ParseMode.HTML
        )

        dialog_manager.show_mode = ShowMode.DELETE_AND_SEND

        await dialog_manager.switch_to(
            BoilerDialog.boiler_main_menu
        )
