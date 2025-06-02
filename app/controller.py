from fastapi import APIRouter
from fastapi.responses import FileResponse
from app.models import Request
from app.service import main

router = APIRouter()

@router.post("/request_insights")
async def request_insights(request: Request):
    print("At post request", request)
    return await main(request)

@router.get("/get_chart")
async def get_chart():
    return FileResponse('file.html')