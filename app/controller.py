from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models import Request
from app.service import main
from fastapi import Request as FastAPIRequest


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/request_insights")
async def request_insights(request: Request):
    # print("At post request", request)
    return await main(request)

@router.get("/get_chart", response_class=HTMLResponse)
async def get_chart(request: FastAPIRequest):
    return templates.TemplateResponse("index.html", {"request": request})
