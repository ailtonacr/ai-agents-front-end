from dataclasses import dataclass, field
import datetime


@dataclass
class Message:
    role: str
    text: str
    timestamp: None | datetime.datetime = field(default_factory=datetime.datetime.now)
