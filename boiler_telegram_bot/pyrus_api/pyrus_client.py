import requests

from db_configuration.models.pyrus import PyrusToken
from settings import pyrus_standard_url


class PyrusClient:
    BASE_URL = pyrus_standard_url

    @staticmethod
    def get_new_token_by_login() -> str | None:
        login_data = PyrusToken.get_login_data()
        if not login_data:
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
        token = PyrusToken.get_token()
        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"Bearer {token}"
        kwargs["headers"] = headers

        url = f"{PyrusClient.BASE_URL}/{endpoint.lstrip('/')}"
        response = requests.request(method.upper(), url, **kwargs)

        if response.status_code == 401:
            new_token = PyrusClient.get_new_token_by_login()
            if new_token:
                PyrusToken.update_token(old_token=token, new_token=new_token)
                headers["Authorization"] = f"Bearer {new_token}"
                kwargs["headers"] = headers
                response = requests.request(method.upper(), url, **kwargs)

        return response

