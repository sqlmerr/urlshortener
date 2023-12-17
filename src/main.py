import uvicorn
import os
import dotenv

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.database import Link
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI(
    version="0.2"
)
dotenv.load_dotenv()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup():
    mongo = AsyncIOMotorClient(os.getenv("MONGO_URL"))
    await init_beanie(database=mongo.urlshortener, document_models=[Link])


@app.get("/")
async def root(request: Request):
    # return {"message": "Hello World!"}
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == '__main__':
    uvicorn.run(app)
