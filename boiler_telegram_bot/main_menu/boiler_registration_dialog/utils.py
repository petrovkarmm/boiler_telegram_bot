import re


def is_valid_inn_organization(inn: str) -> bool:
    """Проверка корректности ИНН юридического лица (10 цифр с контрольной суммой)."""
    if not re.fullmatch(r"\d{10}", inn):
        return False

    coefficients = [2, 4, 10, 3, 5, 9, 4, 6, 8]
    checksum = sum(int(digit) * coef for digit, coef in zip(inn[:9], coefficients)) % 11 % 10
    return checksum == int(inn[9])
