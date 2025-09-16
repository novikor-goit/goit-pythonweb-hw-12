class NoSuchEntityException(Exception):

    def __init__(self, field: str, value: int | str):
        self.field = field
        self.value = value
        super().__init__(f"No such entity with {field} {value}")
