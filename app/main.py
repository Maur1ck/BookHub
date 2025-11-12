from fastapi import FastAPI

from app.api.books import router as books_router


app = FastAPI(
    title="BookHub",
    description="Онлайн библиотека",
)
app.include_router(books_router)
