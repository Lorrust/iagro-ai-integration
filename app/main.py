from fastapi import FastAPI
from app.routes import all_routes

app = FastAPI(
    title="FastAPI Integration API",
    description="Receive messages and images, and return responses from the OpenAI API.",
    version="1.0.0",
)

for router in all_routes:
    app.include_router(router)
