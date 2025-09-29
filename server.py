import asyncio
import logging
import os
import threading
import time
from faster_whisper import WhisperModel
from flask import Flask, request

APP_NAME = "transcriber-server"
DATA_FOLDER = "./data"
MODEL_FOLDER = "./model"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.getLogger("waitress").setLevel(logging.INFO)
logger = logging.getLogger("transcriber-server")
logger.setLevel(logging.INFO)
app = Flask(APP_NAME)
os.makedirs(DATA_FOLDER, exist_ok=True)

model = WhisperModel(model_size_or_path=MODEL_FOLDER, device=os.environ["DEVICE"])


def transcribe(job_id, input_file_path):
    logger.info(f"{job_id} - Entering transcribe()")

    file_path = os.path.join(DATA_FOLDER, f"{job_id}.txt")
    segments, _ = model.transcribe(input_file_path, language=os.environ["LANGUAGE"])
    with open(file_path, "w", encoding="utf-8") as file:
        for segment in segments:
            file.write(segment.text)

    logger.info(f"{job_id} - Leaving transcribe()")


@app.route("/download/<int:job_id>", methods=["GET"])
def download(job_id):
    logger.info(f"{job_id} - Entering download() ... ")
    file_path = os.path.join(DATA_FOLDER, f"{job_id}.txt")
    if os.path.isfile(file_path):
        if os.stat(file_path).st_size > 0:
            with open(file_path, "r", encoding="utf-8") as file:
                logger.info(f"{job_id} - Leaving download() = 200")
                return file.read(), 200
        else:
            logger.info(f"{job_id} - Leaving download() = 404")
            return "{\"error\" : \"Job is being processed\"}\n", 404
    else:
        logger.info(f"{job_id} - Leaving download() = 404")
        return "{\"error\" : \"Job does not exist\"}\n", 404


@app.route("/upload", methods=["POST"])
def upload():
    logger.info("Entering upload()")
    if "file" not in request.files:
        return "{\"error\" : \"File is not found in the request\"}\n", 400

    job_id = str(int(time.time()))
    file_name = f"{job_id}.mp3"
    file_path = os.path.join(DATA_FOLDER, file_name)
    request.files["file"].save(file_path)

    logger.info(f"... size({file_name})={os.stat(file_path).st_size}")
    threading.Thread(target=transcribe, args=(job_id, file_path)).start()

    logger.info(f"{job_id} - Leaving upload(...)")
    return "{\"job_id\": " + job_id + "}\n", 200


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=os.environ["PORT"])
