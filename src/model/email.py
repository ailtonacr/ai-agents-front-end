import re


class Email:
    @staticmethod
    def validate(email: str | None) -> str | None:
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if email is None or len(email) == 0:
            return None
        if len(email) > 1 and not re.match(pattern, email):
            raise ValueError("Email inválido, por favor, verifique o email informado.")
        return email

    def __new__(cls, email: str | None) -> str | None:
        return cls.validate(email)
