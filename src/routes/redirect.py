from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from src.database import Link, get_url


router = APIRouter()

@router.get("/{code}")
async def redirect(code: str):
    url = await get_url(code)
    if not url:
        return {"error": "The requested page was not found"}
    
    return RedirectResponse(url.link)
