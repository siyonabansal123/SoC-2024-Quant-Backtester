from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from data import DataHandler
from trading import Trading_Execution, strategy_build
 




app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Global storage for preprocessed data
preprocessed_data = None
preprocessed_ticker = None
preprocessed_start_date = None
preprocessed_end_date = None


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process_data/", response_class=HTMLResponse)
async def process_data(request: Request, ticker: str = Form(...), start_date: str = Form(...), end_date: str = Form(...)):
    global preprocessed_data, preprocessed_ticker, preprocessed_start_date, preprocessed_end_date
    data_handler = DataHandler(ticker, start_date, end_date)
    data = data_handler.fetch_data()
    data_summary = data_handler.data_characteristics()
    preprocessed_data = data_handler.missing_value_handler()
    plot_path = data_handler.performance_analysis()  # Get plot path
    
    # Convert data summary to HTML table
    data_summary_html = data_summary.to_html(classes="table table-striped")
    
    # Save preprocessed data details
    preprocessed_ticker = ticker
    preprocessed_start_date = start_date
    preprocessed_end_date = end_date
    
    return templates.TemplateResponse("preprocess.html", {"request": request, "data_summary": data_summary_html, "plot_path": plot_path})



@app.post("/run_strategy/", response_class=HTMLResponse)
async def run_strategy(request: Request):
    global preprocessed_data, preprocessed_ticker, preprocessed_start_date, preprocessed_end_date
    if preprocessed_data is None:
        return HTMLResponse("No preprocessed data available. Please preprocess the data first.", status_code=400)

    df = strategy_build(preprocessed_data)
    
    # Use the saved ticker, start date, and end date
    trading_execution = Trading_Execution(df, preprocessed_ticker, preprocessed_start_date, preprocessed_end_date)
    returns = trading_execution.run()
    
    returns_html = returns.to_frame().to_html(classes="table table-striped")
    
    return templates.TemplateResponse("results.html", {"request": request, "returns": returns_html})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)