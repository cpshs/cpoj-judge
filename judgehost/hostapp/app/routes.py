from fastapi import FastAPI, Request

def register_routes(app: FastAPI):

    @app.get("/")
    def hello():
        return {"message": "Greeting From CPOJ Judge Host."}

    @app.get("/bind")
    async def bind(request: Request):
        data = await request.json()
        app.state.url = data['server_url']
        return {"message": "Sucessful!"}

    @app.get("/queue")
    def get_queue(request: Request):
        return {"tasks_num": app.state.queue.qsize()}

    @app.post("/submit")
    async def push_queue(request: Request):
        data = await request.json()
        app.state.queue.put(data)
        return {"message": "queued"}
