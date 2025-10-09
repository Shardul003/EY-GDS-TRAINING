from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging
import time
import traceback

app = FastAPI()

# ---------------- CONFIGURE STRUCTURED LOGGING ----------------
logging.basicConfig(
    filename="server.log",
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)

# Initialize global page visit tracker
page_hits = 0

# ---------------- REQUEST TRACKING MIDDLEWARE ----------------
@app.middleware("http")
async def request_logger(request: Request, next_call):
    global page_hits
    start_time = time.time()

    # Increment hit count
    page_hits += 1
    logging.info(f"Page Hit #{page_hits} | Endpoint: {request.url.path}")

    try:
        response = await next_call(request)
    except Exception as err:
        elapsed = round(time.time() - start_time, 3)
        logging.error(
            f"Error in {request.method} {request.url.path}: {str(err)}\n{traceback.format_exc()}"
        )
        raise err

    # Log request duration and add header
    elapsed = round(time.time() - start_time, 3)
    logging.info(
        f"{request.method} {request.url.path} | Status: {response.status_code} | Took: {elapsed}s"
    )

    response.headers["X-Visit-Count"] = str(page_hits)
    return response


# ---------------- ROUTES ----------------
@app.get("/")
def index():
    return {
        "message": "Hello from FastAPI!",
        "visit_total": page_hits,
        "note": "Reload the page to see the visit counter increase."
    }


@app.get("/hits")
def fetch_hits():
    # Return total page hit count
    return {"visit_total": page_hits}


# ---------------- UNIVERSAL EXCEPTION HANDLER ----------------
@app.exception_handler(Exception)
async def catch_all_exceptions(request: Request, err: Exception):
    logging.error(
        f"Unhandled Exception at {request.url.path}: {str(err)}\n{traceback.format_exc()}"
    )
    return JSONResponse(
        status_code=500,
        content={"error": "Something went wrong.", "details": str(err)},
    )
