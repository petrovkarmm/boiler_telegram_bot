import re


async def normalize_phone_number(phone: str) -> str | None:
    # Удаляем все нецифровые символы
    digits = re.sub(r"\D", "", phone)

    if len(digits) == 11 and digits.startswith("8"):
        return "+7" + digits[1:]
    elif len(digits) == 11 and digits.startswith("7"):
        return "+7" + digits[1:]
    elif len(digits) == 11 and digits.startswith("9"):
        return "+7" + digits
    elif len(digits) == 10 and digits.startswith("9"):
        return "+7" + digits
    elif len(digits) == 12 and digits.startswith("7"):
        return "+" + digits
    else:
        return None
