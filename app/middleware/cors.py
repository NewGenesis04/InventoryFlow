from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",
    "https://localhost:3000",
    "http://localhost:8000",
    "https://localhost:8000"
]

def add_cors_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )