import threading
import logging
import requests
import json

from time import sleep

from fastapi import FastAPI

def launch_scheduler(app: FastAPI):
    runner = threading.Thread(target=scheduler, args=(app, ))
    runner.daemon = True
    runner.start()

def scheduler(app: FastAPI):
    logger = logging.getLogger("scheduler")
    logging.basicConfig(level=logging.INFO)

    while job := app.state.queue.get():
        submission_id = job['id']
        task_payload = job['task']
        for cmd in task_payload['cmd']:
            cmd['procLimit'] = 64
            cmd['files'] = [
                {"content": ""},
                {"name": "stdout", "max": 102400},
                {"name": "stderr", "max": 102400}
            ]
            cmd['copyOut'] = ["stdout"]
            cmd['env'] = ["PATH=/usr/bin:/bin"]
        try:
            response = requests.post("http://go-judge:5050/run",
                                     json=task_payload,
                                     headers={"Content-Type": "application/json"})
            result = response.json()

            logger.info(f"任務 {submission_id} 完成，結果：{result}")
        except Exception as e:
            logger.error(f"任務 {submission_id} 發生錯誤：{e}")
