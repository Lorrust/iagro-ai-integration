from fastapi import FastAPI
from app.routes import all_routes
import uvicorn

app = FastAPI(
    title="FastAPI Integration API",
    description="Receive messages and images, and return responses from the OpenAI API.",
    version="1.0.0",
)

for router in all_routes:
    app.include_router(router)

def start():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
