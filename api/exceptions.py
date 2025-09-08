from starlette.responses import JSONResponse


class NoSuchEntityException(Exception):
    def __init__(self, entity_id: int):
        self.entity_id = entity_id
        super().__init__(f"No such entity with ID {entity_id}")
