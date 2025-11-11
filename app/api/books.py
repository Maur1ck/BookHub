from fastapi import APIRouter

router = APIRouter(prefix="/books", tags=["Книги"])


@router.get("/")
def get_books():
    return {"message": "Hello World"}
