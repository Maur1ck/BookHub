import uvicorn
from fastapi import FastAPI

from app.api.books import router as books_router


app = FastAPI(
    title="BookHub",
    description="Онлайн библиотека",
)
app.include_router(books_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
