import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(
    version="0.1"
)

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request):
    # return {"message": "Hello World!"}
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == '__main__':
    uvicorn.run(app)
