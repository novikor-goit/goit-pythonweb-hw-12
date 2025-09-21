import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from rich.logging import RichHandler

from src.api.exceptions import NoSuchEntityException
from src.api.routes import contacts
from src.api.routes.auth import router as auth_router
from src.api.routes.users import router as users_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(NoSuchEntityException)
async def handle_no_such_entity(request, exc: NoSuchEntityException):
    return JSONResponse(
        status_code=404,
        content={"message": f"{exc.message}"},
    )


app.include_router(contacts.router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(users_router, prefix="/api")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.getLogger().handlers = [RichHandler()]

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
