from dataclasses import dataclass


@dataclass
class Raip:
    title: str
    number: str
    pub_date: str
    href: str

    def __repr__(self) -> str:
        return f' РАИП №{self.number} от {self.pub_date}'
