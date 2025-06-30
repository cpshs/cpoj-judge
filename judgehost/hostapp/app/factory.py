from queue import Queue
import random
import string

from fastapi import FastAPI

from .routes import register_routes
from .scheduler import launch_scheduler


def create_app() -> FastAPI:
    app = FastAPI()
    app.state.queue = Queue()
    app.state.secret = ''.join(random.choices(string.ascii_letters + string.digits, k=64))
    register_routes(app)

    @app.on_event("startup")
    def start_scheduler():
        launch_scheduler(app)

    return app
