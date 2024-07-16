from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from data import DataHandler
import pandas as pd
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process_data/", response_class=HTMLResponse)
async def process_data(request: Request, ticker: str = Form(...), start_date: str = Form(...), end_date: str = Form(...)):
    data_handler = DataHandler(ticker, start_date, end_date)
    data = data_handler.fetch_data()
    data_summary = data_handler.data_characteristics()
    cleaned_data = data_handler.missing_value_handler()
    plot_path = data_handler.performance_analysis()  # Get plot path
    
    # Convert data summary to HTML table
    data_summary_html = data_summary.to_html(classes="table table-striped")
    
    return templates.TemplateResponse("results.html", {"request": request, "data_summary": data_summary_html, "plot_path": plot_path})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)