from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

from app.graph import build_graph
from app.schemas import TickerRequest

app = FastAPI(title="Alpha-Agent Pipeline Ecosystem", version="2.0")
graph = build_graph()

templates = Jinja2Templates(directory="app/templates")

# Ensure the local artifact storage directory exists dynamically
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
    ticker_input = req.ticker.strip().upper()
    
    # 1. Initialize full structural context state
    initial_state = {
        "ticker": ticker_input,
        "validation_status": "PENDING",
        "market": {},
        "sentiment": {},
        "evaluation": {},
        "decision": {},
        "report_path": ""
    }

    try:
        # 2. Invoke compiled StateGraph sequentially through all guardrail blocks
        result = graph.invoke(initial_state)

        # 3. Format generated file artifact paths cleanly for frontend down-streams
        report_path = result.get("report_path", "")
        if report_path:
            filename = os.path.basename(report_path)
            result["report_path"] = f"/reports/{filename}"
        print(result)

        # 4. Return complete data map expected by renderCard() in index.html
        return {
            "ticker": result.get("ticker"),
            "market": result.get("market"),
            "sentiment": result.get("sentiment"),
            "evaluation": result.get("evaluation"),
            "decision": result.get("decision"),
            "report_path": result.get("report_path")
        }

    except ValueError as val_err:
        # Catch regex failures from validation_agent and return explicit 400 Bad Request
        raise HTTPException(status_code=400, detail=str(val_err))
    except Exception as e:
        # Catch runtime crashes globally to protect application uptime
        raise HTTPException(status_code=500, detail=f"Core Pipeline Execution Error: {str(e)}")