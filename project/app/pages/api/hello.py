from fasthtml.core import APIRouter

rt = APIRouter()

@rt("/api/hello")
def get(request):
    return {"message": "Hello, World!"}