import enum

class Gender(enum.Enum):
    MALE='MALE'
    FEMALE='FEMALE'
    OTHER='OTHER'

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]