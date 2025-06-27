from fastapi import FastAPI
from .routes import register_routes
from .scheduler import launch_scheduler
from queue import Queue

def create_app() -> FastAPI:
    app = FastAPI()
    app.state.queue = Queue()
    register_routes(app)

    @app.on_event("startup")
    def start_scheduler():
        launch_scheduler(app)

    return app
