from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import asyncio
from scanner import DomainScanner

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/scan", response_class=HTMLResponse)
async def scan(request: Request, domain: str = Form(...)):
    # Run the domain scanner
    scanner = DomainScanner(domain)
    scan_results = await scanner.run_all()
    
    # Compute overall score (average of metrics), clamp to 0-100
    vals = [scan_results.get(k, 0) for k in ("ssl", "dns", "surface", "exposure", "rep")]
    total = round(sum(vals) / len(vals)) if vals else 0
    total = max(0, min(100, int(total)))
    scan_results["score"] = total
    
    return templates.TemplateResponse("components/results.html", {
        "request": request, 
        "data": scan_results
    })