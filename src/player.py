from dataclasses import dataclass
from enums import Icon


@dataclass
class MiffyPlayer():
    icon: Icon

    def __str__(self):
        return f"{self.icon.name.upper()}"
