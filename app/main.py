from fastapi import FastAPI

from app.api.books import router as books_router
from app.api.auth import router as auth_router


app = FastAPI(
    title="BookHub",
    description="Онлайн библиотека",
)
app.include_router(auth_router)
app.include_router(books_router)
