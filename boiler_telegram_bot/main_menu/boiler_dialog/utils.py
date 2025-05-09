import re


async def normalize_phone_number(phone: str) -> str | None:
    digits = re.sub(r"\D", "", phone)

    if len(digits) != 11:
        return None

    if digits.startswith("8") or digits.startswith("7"):
        return "+7" + digits[1:]
    elif digits.startswith("9"):
        return "+7" + digits
    else:
        return None
