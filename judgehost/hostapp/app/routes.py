import os
import shutil
import tarfile

from fastapi import FastAPI, Request


def register_routes(app: FastAPI):

    @app.get("/")
    def hello():
        return {"secret": app.state.secret}

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

    @app.get("/query_testdata/{hash_value}")
    def query_testdata(hash_value: str):
        problem_path = Path(PROBLEMS_DIR) / hash_value
        exists = problem_path.exists() and problem_path.is_dir()
        return {"exists": exists}

    @app.post("/upload_testdata")
    async def upload_testdata(hash_value: str = Request(...), file: UploadFile = File(...)):
        dest_dir = Path(PROBLEMS_DIR) / hash_value
        if dest_dir.exists():
            shutil.rmtree(dest_dir)
        dest_dir.mkdir(parents=True)

        tmp_tar = dest_dir / file.filename
        with open(tmp_tar, "wb") as f:
            f.write(await file.read())

        try:
            with tarfile.open(tmp_tar, "r:gz") as tar:
                tar.extractall(path=dest_dir)
        except tarfile.TarError:
            raise HTTPException(status_code=400, detail="Invalid tar.gz file")

        tmp_tar.unlink()
        return {"message": "uploaded and extracted", "path": str(dest_dir)}
   
