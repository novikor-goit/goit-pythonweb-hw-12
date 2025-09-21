class NoSuchEntityException(Exception):

    def __init__(self, field: str, value: int | str):
        self.field = field
        self.value = value
        self.message = f"No such entity with {field} {value}"
        super().__init__(self.message)
