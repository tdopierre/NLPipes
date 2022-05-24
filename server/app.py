import json
from typing import Dict
from src.util import get_logger

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from src.clustering import models
from src.ml.embedding import embedding_models
from src.process import MainProcess, PipeConfig
from src.socket import client as socket_client

logger = get_logger(__name__)

processes: Dict[str, MainProcess] = dict()

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sio = SocketIO(app, cors_allowed_origins="*")


@app.route("/process", methods=["POST"])
def process():
    # Show received form
    logger.debug(f"Received form {request.form}")

    # Show received file(s?)
    logger.debug(f'Received files {request.files}')
    # logger.debug(f'Received files {next(request.files.items())}')

    # assert len(request.files) == 1, 'More than 1 file received!'
    files = {
        file_id: file
        for file_id, file in request.files.items()
    }
    logger.debug(f'files {files} {len(files)}')

    # file = request.files[list(request.files.keys())[0]]
    # file_name = file.filename
    # corpus = file.read().decode().split('\n')
    # corpus = [c.strip() for c in corpus if len(c.strip())]

    # Load run name
    name = request.form["name"]
    id = request.form["id"]

    # Pipes
    pipes = json.loads(request.form["pipes"])
    pipes_configs = [
        PipeConfig(
            pipe_type=pipe["pipe_type"],
            config=pipe["config"],
            name=pipe["name"],
            id=pipe["id"],
            dependencies=pipe.get("dependencies", list())
        )
        for pipe in pipes
    ]
    # Main process
    global processes

    processes[id] = MainProcess(
        config=dict(
            name=name,
            id=id,
            pipes=pipes
        ),
        pipe_configs=pipes_configs,
        files=files,
        name="main",
        x=dict(),
        id=id

    )
    processes[id].start()

    return jsonify(processes[id].export_config())


@app.route("/processes/<thread_id>", methods=["DELETE"])
def delete_process(thread_id):
    socket_client.emit('delete-process', {
        "id": thread_id
    })
    try:
        processes.pop(thread_id)
    except KeyError:
        pass
    return '', 200


@app.route("/embedders", methods=["GET"])
def get_embedders():
    return jsonify(list(embedding_models.keys())), 200


@app.route("/embedders/transformers", methods=["GET"])
def get_embedders_transformers():
    return jsonify([
        'bert-base-multilingual-cased',
        'sentence-transformers/stsb-roberta-large',
        'camembert-base',
        'distiluse-base-multilingual-cased-v1'
    ]), 200


@app.route("/models", methods=["GET"])
def get_models():
    return jsonify(list(models.keys())), 200


@app.route("/tellme", methods=["POST"])
def tell_me():
    return "", 200


@app.route("/processes", methods=["GET"])
def get_processes():
    global processes
    return jsonify([process.export_config() for thread_id, process in processes.items()][::-1])


@app.route("/status/<thread_id>")
def status(thread_id):
    global processes

    return str(processes[thread_id].status)


@app.route("/config/<thread_id>")
def thread_config(thread_id):
    global processes
    return jsonify({
        "config": processes[thread_id].export_config()
    })


@app.route("/result/<thread_id>")
def thread_result(thread_id):
    global processes
    # print(f'results are {processes[thread_id].results()}')
    # logger.debug(f"last pipe is of type {type(processes[thread_id].pipes[-1])}")
    return jsonify({
        "result": processes[thread_id].results_json(),
        "config": processes[thread_id].export_config()
    })


@app.route("/result/<thread_id>/<pipe_id>")
def pipe_result(thread_id, pipe_id):
    logger.error(f"Asked to look for result {thread_id}/{pipe_id}")
    global processes
    for _, pipe in processes[thread_id].processes.items():
        logger.error(f"Inspecting pipe with id {pipe.id}")
        if pipe.id == pipe_id:
            logger.error(f"{pipe.id} matches {pipe_id}")
            return jsonify({
                "result_data": pipe.results_json(),
                "result_type": pipe.results_type,
                "pipe_name": pipe.name
            })

    return jsonify({
        "message": "Process / Pipe not found"
    }), 404


@app.route("/download")
def download():
    return send_file("/tmp/toto.pdf")


def other_func():
    return {
        "json": "json"
    }


# Run App
if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8001", debug=True)
