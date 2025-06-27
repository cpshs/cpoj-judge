from fastapi import FastAPI

def register_routes(app: FastAPI):
    @app.get("/")
    def hello():
        return {"message": "Hello, World from factory"}
