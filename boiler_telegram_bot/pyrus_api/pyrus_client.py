import hashlib
import os
import time

import requests

from boiler_telegram_bot.db_configuration.models.pyrus import PyrusToken
from boiler_telegram_bot.settings import pyrus_standard_url, pyrus_login
from boiler_telegram_bot.tg_logs.logger import bot_logger


class PyrusClient:
    BASE_URL = pyrus_standard_url

    @staticmethod
    def get_new_token_by_login() -> str | None:
        login_data = PyrusToken.get_login_data()
        if not login_data:
            bot_logger.warning(
                'Отсутствуют данные по токену.'
            )
            return None

        login, security_key = login_data
        response = requests.post(
            f"{PyrusClient.BASE_URL}/auth",
            json={"login": login, "security_key": security_key}
        )

        if response.status_code == 200:
            return response.json().get("access_token")
        return None

    @staticmethod
    def request(method: str, endpoint: str, **kwargs):
        start_time = time.time()

        token = PyrusToken.get_token()
        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"Bearer {token}"
        kwargs["headers"] = headers

        url = f"{PyrusClient.BASE_URL}/{endpoint.lstrip('/')}"
        try:
            response = requests.request(method.upper(), url, **kwargs)
            if response.status_code == 401:
                bot_logger.warning(f"401 Unauthorized. Refreshing token and retrying: {method.upper()} {url}")
                new_token = PyrusClient.get_new_token_by_login()
                if new_token:
                    PyrusToken.update_token(pyrus_login=pyrus_login, new_token=new_token)
                    headers["Authorization"] = f"Bearer {new_token}"
                    kwargs["headers"] = headers
                    response = requests.request(method.upper(), url, **kwargs)
        except Exception as e:
            bot_logger.exception(f"[PYRUS REQUEST ERROR] {method.upper()} {url} | Exception: {e}")
            raise

        duration = round(time.time() - start_time, 2)
        bot_logger.info(
            f"[PYRUS] {method.upper()} {url} | Status: {response.status_code} | "
            f"Time: {duration}s | Request kwargs: {kwargs} | Response: {response.text[:300]}"
        )

        return response

    @staticmethod
    def upload_file(file_path: str, filename: str) -> dict | None:
        if not os.path.isfile(file_path):
            bot_logger.warning(f"Файл {file_path} не найден. Возможно, он был автоматически удалён.")
            return None

        with open(file_path, "rb") as f:
            file_bytes = f.read()
            md5_hash = hashlib.md5(file_bytes).hexdigest()
            files = {"file": (filename, file_bytes, "application/octet-stream")}
            response = PyrusClient.request("POST", "/files/upload", files=files)
            if response.status_code == 200:
                return response.json()
            bot_logger.warning(f"Upload failed: {response.text}")
            return None