from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import all_routes
import uvicorn

app = FastAPI(
    title="OpenAI Integration API",
    description="Receive messages and images, and return responses from the OpenAI API.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in all_routes:
    app.include_router(router)

def start():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
