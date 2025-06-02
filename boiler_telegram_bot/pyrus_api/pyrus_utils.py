import re
from typing import Dict

from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode

from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_states import BoilerDialog
from boiler_telegram_bot.pyrus_api.pyrus_client import PyrusClient
from boiler_telegram_bot.main_menu.boiler_dialog.utils import normalize_phone_number


async def get_form_and_field_id_by_form_name(pyrus_forms_data: dict, form_name: str, fields_name: list):
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

    return None


async def get_client_catalog_id():
    pyrus_catalog_request = PyrusClient.request(
        method='GET', endpoint='/catalogs'
    )

    pyrus_catalog_data = pyrus_catalog_request.json()
    catalogs_data = pyrus_catalog_data.get('catalogs')
    catalogs_data: Dict
    for catalog in catalogs_data:
        if catalog.get('name') == 'Клиенты' and catalog.get('deleted') is False:
            return catalog.get('catalog_id')

    return None


async def find_legal_entity_client_by_organization(callback: CallbackQuery,
                                                   organization_itn: str,
                                                   organization_name: str,
                                                   dialog_manager: DialogManager):
    catalog_id = await get_client_catalog_id()

    if catalog_id:

        clients_catalog_request = PyrusClient.request(
            method='GET', endpoint=f'/catalogs/{catalog_id}'
        )

        clients_catalog_data = clients_catalog_request.json()
        clients_catalog_data: Dict

        clients = clients_catalog_data.get('items', [])
        normalized_itn = re.sub(r'\D', '', organization_itn)
        normalized_name = re.sub(r'\s+', ' ', organization_name.strip().lower())

        for client in clients:
            values = client.get('values', [])
            combined = ' '.join(values).lower()
            combined = re.sub(r'\s+', ' ', combined)

            has_itn = re.search(rf'\b{re.escape(normalized_itn)}\b', combined)
            has_name = re.search(rf'\b{re.escape(normalized_name)}\b', combined)

            if has_itn and has_name:
                return client.get('item_id')

        new_client_data = {
            "upsert": [
                {
                    "values": [
                        organization_name,
                        f'ИНН {organization_itn}'
                    ]
                }]
        }

        adding_new_client_request = PyrusClient.request(
            method='POST', endpoint=f'/catalogs/{catalog_id}/diff', json=new_client_data
        )

        new_pyrus_client_data = adding_new_client_request.json()
        new_pyrus_client_data: True

        if new_pyrus_client_data.get('apply', False) is True:
            return new_pyrus_client_data.get('added')[0].get('item_id')

        return None

    else:
        await callback.message.answer(
            text='⚠️ Упс! Кажется, что-то пошло не так.\n'
                 'Попробуйте позже.',
            parse_mode=ParseMode.HTML
        )

        dialog_manager.show_mode = ShowMode.DELETE_AND_SEND

        await dialog_manager.switch_to(
            BoilerDialog.boiler_main_menu
        )

        return None


async def find_individual_client_by_phone(callback: CallbackQuery,
                                          user_phone: str,
                                          user_name: str,
                                          dialog_manager: DialogManager):
    catalog_id = await get_client_catalog_id()

    if catalog_id:

        clients_catalog_request = PyrusClient.request(
            method='GET', endpoint=f'/catalogs/{catalog_id}'
        )

        clients_catalog_data = clients_catalog_request.json()
        clients_catalog_data: Dict

        clients = clients_catalog_data.get('items', [])
        normalized_phone = await normalize_phone_number(user_phone)
        normalized_name = re.sub(r'\s+', ' ', user_name.strip().lower())

        for client in clients:
            values = client.get('values', [])
            combined = ' '.join(values).lower()
            combined = re.sub(r'\s+', ' ', combined)

            has_phone = re.search(re.escape(normalized_phone), combined)
            has_name = re.search(rf'\b{re.escape(normalized_name)}\b', combined)

            if has_phone and has_name:
                return client.get('item_id')

        new_client_data = {
            "upsert": [
                {
                    "values": [
                        normalized_name,
                        normalized_phone
                    ]
                }]
        }

        adding_new_client_request = PyrusClient.request(
            method='POST', endpoint=f'/catalogs/{catalog_id}/diff', json=new_client_data
        )

        new_pyrus_client_data = adding_new_client_request.json()

        new_pyrus_client_data: True

        if new_pyrus_client_data.get('apply', False) is True:
            return new_pyrus_client_data.get('added')[0].get('item_id')


        return None

    else:
        await callback.message.answer(
            text='⚠️ Упс! Кажется, что-то пошло не так.\n'
                 'Попробуйте позже.',
            parse_mode=ParseMode.HTML
        )

        dialog_manager.show_mode = ShowMode.DELETE_AND_SEND

        await dialog_manager.switch_to(
            BoilerDialog.boiler_main_menu
        )

        return None


async def send_form_task(callback: CallbackQuery,
                         user_name: str,
                         user_phone: str,
                         task_title: str,
                         task_description: str,
                         user_address: str,
                         firm_type: str,
                         dialog_manager: DialogManager,
                         tmp_file_path: str = None,
                         filename: str = None,
                         organization_name: str = None,
                         organization_itn: str = None):
    await dialog_manager.switch_to(
        BoilerDialog.boiler_send_task_waiting_status
    )

    pyrus_forms_response = PyrusClient.request('GET', '/forms')
    if pyrus_forms_response.status_code == 200:
        forms_data = pyrus_forms_response.json()
        pyrus_id_data = await get_form_and_field_id_by_form_name(pyrus_forms_data=forms_data,
                                                                 form_name='лиды с сайта',
                                                                 fields_name=['проблема', 'описание', 'имя', 'телефон',
                                                                              'адрес', 'клиенты', 'приложения'])
        if not pyrus_id_data:
            await callback.message.answer(
                text='⚠️ Упс! Кажется, что-то пошло не так.\n'
                     'Попробуйте позже.',
                parse_mode=ParseMode.HTML
            )

            dialog_manager.show_mode = ShowMode.DELETE_AND_SEND

            await dialog_manager.switch_to(
                BoilerDialog.boiler_main_menu
            )

        if firm_type == 'legal_entity':
            client_id = await find_legal_entity_client_by_organization(
                callback=callback,
                dialog_manager=dialog_manager,
                organization_name=organization_name,
                organization_itn=organization_itn
            )
        else:
            client_id = await find_individual_client_by_phone(
                callback=callback,
                dialog_manager=dialog_manager,
                user_name=user_name,
                user_phone=user_phone
            )

        fields = [
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
        ]

        if client_id:
            fields.append({
                'id': pyrus_id_data.get('Клиенты'),
                'value': {
                    'item_id': client_id
                }
            })

        if tmp_file_path and filename:
            pyrus_files_data = PyrusClient.upload_file(
                file_path=tmp_file_path, filename=filename
            )

            if pyrus_files_data:
                pyrus_guid = pyrus_files_data['guid']
                fields.append(
                    {
                        'id': pyrus_id_data.get('Приложения'),
                        'value': [f'{pyrus_guid}']

                    }
                )

        pyrus_task_data = {
            'form_id': pyrus_id_data.get('form_id'),
            'fields': fields
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
        await callback.message.answer(
            text='⚠️ Упс! Кажется, что-то пошло не так.\n'
                 'Попробуйте позже.',
            parse_mode=ParseMode.HTML
        )

        dialog_manager.show_mode = ShowMode.DELETE_AND_SEND

        await dialog_manager.switch_to(
            BoilerDialog.boiler_main_menu
        )


async def send_task_comment(task_id: int, file_guid: str):
    data = {
        "text": 'Пользователь загрузил файл.',
        "attachments": [file_guid],
    }
    response = PyrusClient.request("POST", f"/tasks/{task_id}/comments", json=data)
    return response.json()
