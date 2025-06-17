from .chat import router as chat_router
from .chroma import router as chroma_router
from .analysis import router as analysis_router

all_routes = [chat_router, chroma_router, analysis_router]
