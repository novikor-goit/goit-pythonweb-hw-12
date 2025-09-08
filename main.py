import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from rich.logging import RichHandler

from api.exceptions import NoSuchEntityException
from api.routes import contacts

app = FastAPI()


@app.exception_handler(NoSuchEntityException)
async def handle_no_such_entity(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": f"No such entity with ID {exc.entity_id}"},
    )


app.include_router(contacts.router, prefix="/api")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.getLogger().handlers = [RichHandler()]

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
