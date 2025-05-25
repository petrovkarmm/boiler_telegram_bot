import re


def is_valid_inn(inn: str) -> bool:
    """Проверка корректности ИНН:
    - 10 цифр — для юридических лиц
    - 12 цифр — для индивидуальных предпринимателей и физлиц
    """
    if re.fullmatch(r"\d{10}", inn):
        return _validate_inn_legal_entity(inn)
    elif re.fullmatch(r"\d{12}", inn):
        return _validate_inn_individual(inn)
    return False


def _validate_inn_legal_entity(inn: str) -> bool:
    coefficients = [2, 4, 10, 3, 5, 9, 4, 6, 8]
    checksum = sum(int(d) * c for d, c in zip(inn[:9], coefficients)) % 11 % 10
    return checksum == int(inn[9])


def _validate_inn_individual(inn: str) -> bool:
    coefficients_1 = [7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
    coefficients_2 = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8]

    checksum_1 = sum(int(d) * c for d, c in zip(inn[:10], coefficients_1)) % 11 % 10
    checksum_2 = sum(int(d) * c for d, c in zip(inn[:11], coefficients_2)) % 11 % 10

    return checksum_1 == int(inn[10]) and checksum_2 == int(inn[11])
