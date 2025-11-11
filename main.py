import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title="BookHub",
    description="Онлайн библиотека",
)


@app.get("/")
def read_root():
    return {"message": "Start project"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
