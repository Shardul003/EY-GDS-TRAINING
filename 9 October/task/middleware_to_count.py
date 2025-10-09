from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging
import time
import traceback
app = FastAPI()
visit_counts = 0
logging.basicConfig(
    filename="app.log",
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)

@app.middleware("http")
async  def count_visits(request: Request, call_next):
    global visit_counts
    visit_counts += 1

    logging.info(f"Visit count : {visit_counts}")
    response = await call_next(request)

    return response

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    try:
        response = await call_next(request)
    except Exception as e:
        duration = round(time.time() - start, 3)
        logging.error(
            f"Exception in {request.method} {request.url.path}: {str(e)}\n{traceback.format_exc()}"
        )
        raise e
    duration = round(time.time() - start, 3)
    logging.info(
        f"{request.method} {request.url.path} | Status: {response.status_code} | Duration: {duration}s"
    )
    return response
students = [{"id": 1, "name": "Rahul"}, {"id": 2, "name": "Neha"}]
@app.get("/students")
def get_students():
    logging.info("Fetching all students from database...")
    return students

@app.get("/visits")
def get_visit_counts():
    global visit_counts
    return {"visit_counts": visit_counts}

@app.get("/error-demo")
def error_demo():
    raise ValueError("Simulated error for testing logs")

# ---------------- GLOBAL EXCEPTION HANDLER ----------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(
        f"Unhandled error in {request.url.path}: {str(exc)}\n{traceback.format_exc()}"
    )
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "detail": str(exc)},
    )
