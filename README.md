# DL Streamer Desktop App (GUI)

Demo Video: https://youtu.be/XXUsDnoPa54

A lightweight desktop GUI for running Intel DL Streamer pipelines using Docker. Supports Crowd Detection, Pose Estimation, Face Detection + Re-ID, and Attribute Classification on local video files.

---

##  Features

- GUI built with PySimpleGUI
- Runs DL Streamer pipelines inside a Docker container
- Supports uploading local video files
- Modes available:
  - **Crowd Detection** (`person-detection-0200`)
  - **Attribute Classification** (`person-attributes-recognition-crossroad-0234`)
  - **Pose Estimation** (`human-pose-estimation-0001`)
  - **Face Detection + Re-ID** (`face-detection-retail-0004` + `face-reidentification-retail-0095`)
- Uses OpenVINO IR models (FP16)
- Logs detection counts in the GUI console

---

##  Project Structure

```text
dlstreamer_app/
├── dlstreamer_desktop_app.py     # GUI + pipeline launcher
├── crowd_counter.py              # Optional standalone crowd counter
├── Dockerfile                    # Build container locally (optional)
├── sample.mp4                    # Sample video for testing
├── models/                       # OpenVINO IR Models (.xml/.bin)
│   ├── person-detection-0200.{xml,bin}
│   ├── person-attributes-recognition-crossroad-0234.{xml,bin}
│   ├── human-pose-estimation-0001.{xml,bin}
│   ├── face-detection-retail-0004.{xml,bin}
│   └── face-reidentification-retail-0095.{xml,bin}
└── README.md
```

---

##  Getting Started

```bash
# Step 1: Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Step 2: Install requirements
pip install -r requirements.txt

# Step 3: Launch the GUI
python3 dlstreamer_desktop_app.py
```

---

##  Docker Container Setup

```bash
docker pull intel/dlstreamer:2025.0.1.2-ubuntu22

# Or build custom image:
docker build -t dlstreamer_gui .
```

---

## 📊 Benchmark Example

Run inside container or OpenVINO env:

```bash
benchmark_app -m models/person-detection-0200.xml -d CPU -hint none -nireq 2 -nstreams 2
```

---

##  Notes

- Ensure you have `xhost +` access for GUI rendering inside container.
- You must have Docker installed and user added to the `docker` group.
- Set up models manually or via Open Model Zoo tools.

---

##  Acknowledgments

- Intel® DL Streamer
- OpenVINO™ Toolkit
- PySimpleGUI for GUI
  
## Sample Output

<img width="609" height="431" alt="result" src="https://github.com/user-attachments/assets/e5c6ad93-b349-4069-abb7-cb188faf1c2d" />
