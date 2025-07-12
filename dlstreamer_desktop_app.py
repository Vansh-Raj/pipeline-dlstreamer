import PySimpleGUI as sg
import os
import subprocess
import time
import signal

# ------------------- Constants -------------------
CONTAINER_NAME = "dlstreamer_app"
IMAGE_NAME = "intel/dlstreamer:2025.0.1.2-ubuntu22"
HOST_PATH = os.path.abspath(".")
CONTAINER_PATH = "/app"

# ------------------- Docker Logic -------------------
def start_docker_container():
    # Check if container is already running
    result = subprocess.run(
        f"docker ps -q -f name={CONTAINER_NAME}", shell=True, capture_output=True, text=True
    )
    if result.stdout.strip():
        print(f"[INFO] Container '{CONTAINER_NAME}' is already running.")
        return

    # Check if container exists but is exited
    result = subprocess.run(
        f"docker ps -aq -f name={CONTAINER_NAME}", shell=True, capture_output=True, text=True
    )
    if result.stdout.strip():
        print(f"[INFO] Starting existing container '{CONTAINER_NAME}'...")
        subprocess.run(f"docker start {CONTAINER_NAME}", shell=True)
        return

    # Otherwise, create a new container
    print("[INFO] Starting new Docker container...")
    cmd = (
        f"docker run -dit --name {CONTAINER_NAME} "
        f"--network=host "
        f"-e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix "
        f"-v \"{HOST_PATH}:{CONTAINER_PATH}\" "
        f"{IMAGE_NAME} bash"
    )
    subprocess.run(cmd, shell=True)
    time.sleep(2)
    print("[INFO] Container started.")

def exec_pipeline_in_container(pipeline_cmd):
    full_cmd = f'docker exec -i {CONTAINER_NAME} bash -c "{pipeline_cmd}"'
    return subprocess.Popen(full_cmd, shell=True, preexec_fn=os.setsid)

# ------------------- GStreamer Pipeline Logic -------------------
def launch_pipeline(video_path, stream_id, mode):
    file_in_container = os.path.join(CONTAINER_PATH, os.path.basename(video_path))

    models = {
        "crowd": "/app/models/person-detection-0200.xml",
        "attribute": "/app/models/person-detection-0200.xml",
        "pose": "/app/models/human-pose-estimation-0001.xml",
        "face": "/app/models/face-detection-retail-0004.xml"
    }

    classifiers = {
        "crowd": "",
        "attribute": "gvaclassify model=/app/models/person-attributes-recognition-crossroad-0234.xml device=CPU !",
        "pose": "",
        "face": "gvaclassify model=/app/models/face-reidentification-retail-0095.xml device=CPU !"
    }

    detection_model = models.get(mode)
    classify_block = classifiers.get(mode, "")

    pipeline = (
        f'gst-launch-1.0 filesrc location="{file_in_container}" ! decodebin ! videoconvert ! '
        f'gvadetect model={detection_model} device=CPU ! '
        f'{classify_block} gvawatermark ! videoconvert ! autovideosink'
    )

    return exec_pipeline_in_container(pipeline)

# ------------------- GUI -------------------
def main():
    print("✅ GUI script started")
    layout = [
        [sg.Text("Upload video:"), sg.Input(key="-FILE-"), sg.FileBrowse()],
        [sg.Text("Number of duplicate streams:"), sg.Slider(range=(1, 8), default_value=1, orientation='h', key='streams')],
        [sg.Text("Choose Use Case:")],
        [sg.Radio("👥 Crowd Detection", "MODE", default=True, key='crowd')],
        [sg.Radio("🧍‍♂️ High Attribute Accuracy", "MODE", key='attribute')],
        [sg.Radio("🤸 Pose Estimation", "MODE", key='pose')],
        [sg.Radio("🙂 Face Detection + ReID", "MODE", key='face')],
        [sg.Button("Start"), sg.Button("Stop All"), sg.Button("Exit")],
        [sg.Multiline(size=(80, 10), key='-LOG-', autoscroll=True, disabled=True)]
    ]

    window = sg.Window("DL Streamer Desktop App", layout)
    processes = []

    def log(msg):
        print(msg)
        window['-LOG-'].update(f"{msg}\n", append=True)

    while True:
        event, values = window.read()

        if event in (sg.WINDOW_CLOSED, "Exit"):
            break

        if event == "Start":
            video = values["-FILE-"]
            num = int(values["streams"])

            if not os.path.isfile(video):
                sg.popup_error("Please select a valid video file.")
                continue

            mode = next(key for key in ['crowd', 'attribute', 'pose', 'face'] if values[key])

            start_docker_container()
            log(f"[INFO] Launching {num} stream(s) for mode: {mode}")

            for i in range(num):
                p = launch_pipeline(video, i, mode)
                log(f"[INFO] Launched pipeline {i+1} with PID {p.pid}")
                processes.append(p)

        if event == "Stop All":
            log("[INFO] Stopping all pipelines...")
            for p in processes:
                try:
                    os.killpg(os.getpgid(p.pid), signal.SIGTERM)
                except Exception as e:
                    log(f"[ERROR] Could not terminate process: {e}")
            processes.clear()

    window.close()
    subprocess.run(f"docker rm -f {CONTAINER_NAME}", shell=True)

if __name__ == "__main__":
    main()
