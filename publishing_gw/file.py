from dataclasses import dataclass
from typing import List, Optional


@dataclass
class File:
    name: str  # e.g. 'camp2023-57136-eng-Lightning_Talks_Session_1_opus.vtt'
    path: str
    size: int
    conference: Optional[str]
    event_local_id: Optional[str]
    language: Optional[str]
    raw: Optional[any]

    @staticmethod
    def from_dict(d):
        parts = d["name"].split("-")
        return File(
            name=d["name"],
            path=d["path"],
            size=d["size"],
            conference=parts[0],
            event_local_id=parts[1],
            language=parts[2],
            raw=d,
        )

    def __post_init__(self):
        """
        Extracts conference acronym, local_id, and language from the filename.
        Assumes filename format like 'camp2023-57136-eng-...'
        """
        parts = self.name.split("-")
        if len(parts) >= 3:
            self.conference = parts[0]
            self.event_local_id = parts[1]
            self.language = parts[2]

    def key(self):
        return f"{self.conference}-{self.event_local_id}"
