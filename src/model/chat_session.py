from dataclasses import dataclass, field
import datetime
from .message import Message
from uuid import uuid5, NAMESPACE_DNS


@dataclass
class ChatSession:
    db_id: str | None
    adk_session_id: str
    user_name: str
    agent_name: str
    created_at: datetime.datetime
    messages: list[Message] = field(default_factory=list)
    summary: str = ""

    def __post_init__(self):
        if not self.db_id or self.db_id is None:
            self.db_id = str(uuid5(NAMESPACE_DNS, f"{self.user_name}-{self.agent_name}-{self.adk_session_id}"))
