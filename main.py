from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import asyncio

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/scan", response_class=HTMLResponse)
async def scan(request: Request, domain: str = Form(...)):
    # Simulating a DS/Security process (like a DNS lookup or API call)
    await asyncio.sleep(1.5) 
    
    # todo replace mock with real scanns 
    mock_data = {
        "ssl": 80,
        "dns": 100,
        "surface": 50,
        "exposure": 100,
        "rep": 100,
    }
    
    return templates.TemplateResponse("components/results.html", {
        "request": request, 
        "data": mock_data
    })