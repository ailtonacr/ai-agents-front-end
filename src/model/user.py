from dataclasses import dataclass
from uuid import uuid5, NAMESPACE_DNS
from .email import Email


@dataclass
class User:
    name: str
    id: str | None
    email: Email | None
    role: str | None
    is_active: bool | None
    password: str | None = None

    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid5(NAMESPACE_DNS, self.name))
