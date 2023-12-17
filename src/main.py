import uvicorn
import os
import dotenv
import uuid

from typing import Optional

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.database import Link, get_url_by_link
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from src.routes import redirect

app = FastAPI(
    version="0.3"
)
app.include_router(redirect.router)


dotenv.load_dotenv()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


def generate_code(lenght = 5) -> str:
    return str(uuid.uuid4().hex)[:lenght]


@app.on_event("startup")
async def startup():
    mongo = AsyncIOMotorClient(os.getenv("MONGO_URL"))
    await init_beanie(database=mongo.urlshortener, document_models=[Link])


@app.get("/")
async def root(request: Request, url: Optional[str] = None):
    if not url:
        return templates.TemplateResponse("index.html", {"request": request})
    else:
        link = await get_url_by_link(url)
        if not link:
            link = Link(
                code=generate_code(),
                link=url
            )
            await link.insert()
        
        return templates.TemplateResponse("index.html", {"request": request, "shorten": f"{request.base_url}{link.code}"})
