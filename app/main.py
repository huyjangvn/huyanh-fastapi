from fastapi import FastAPI
from routers import company, user, task

app = FastAPI()

app.include_router(company.router)
app.include_router(user.router)
app.include_router(task.router)


@app.get("/")
async def health_check():
    return "API Service is up and running!"
