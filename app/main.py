from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

from app.graph import build_graph
from app.schemas import TickerRequest

app = FastAPI()
graph = build_graph()

templates = Jinja2Templates(directory="app/templates")

# Serve the reports folder so PDFs are downloadable
os.makedirs("reports", exist_ok=True)
app.mount("/reports", StaticFiles(directory="reports"), name="reports")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

@app.post("/analyze")
def analyze(req: TickerRequest):
    result = graph.invoke({"ticker": req.ticker})

    report_path = result.get("report_path", "")
    if report_path:
        filename = os.path.basename(report_path)
        result["report_path"] = f"/reports/{filename}"  # Must start with /

    return result