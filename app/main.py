import time
from fastapi import FastAPI, Request
from routers import company, user, task, auth

app = FastAPI()

app.include_router(company.router)
app.include_router(user.router)
app.include_router(task.router)
app.include_router(auth.router)


@app.get("/")
async def health_check():
    return "API Service is up and running!"


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
