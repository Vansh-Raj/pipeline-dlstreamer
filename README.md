DL Streamer Flask Web App
============================

A lightweight Flask web application that uses Intel® DL Streamer to detect and classify people in uploaded videos. It outputs an annotated video and a `meta.json` file containing per-frame classification metadata.

 Features
-----------
- Upload your own video file via browser
- Perform:
  - Person detection (`person-detection-0200`)
  - Attribute classification (`person-attributes-recognition-crossroad-0234`)
- Get:
  - Annotated `output.mp4` with overlays
  - Structured `meta.json` with labels, confidence, and timestamps
- Built with:
  - Flask
  - Intel® DL Streamer (OpenVINO backend)
  - GStreamer

 Models Used
--------------
| Task            | Model Name                                  | Framework         |
|-----------------|----------------------------------------------|-------------------|
| Detection       | person-detection-0200                        | OpenVINO IR (FP16)|
| Classification  | person-attributes-recognition-crossroad-0234| OpenVINO IR (FP16)|

Ensure the .xml and .bin files for each model are placed in the `models/` directory.

 Project Structure
--------------------
dlstreamer-webapp/
├── app.py                    # Flask application
├── requirements.txt          # Python dependencies
├── models/                   # OpenVINO IR models
│   ├── person-detection-0200.xml
│   └── person-attributes-recognition-crossroad-0234.xml
├── static/                   # Output folder (auto-generated)
│   ├── output.mp4
│   └── meta.json
├── uploads/                  # Uploaded videos (auto-generated)
├── templates/
│   └── index.html            # Upload form HTML
└── README.txt                # You're reading it

 Getting Started
------------------
1. Install dependencies:
   pip install -r requirements.txt

2. Run the app:
   python3 app.py

Then visit http://localhost:5000

 Optional: Docker Support
---------------------------
If using Intel’s DL Streamer Docker image:
docker run -it -v $PWD:/workspace -p 5000:5000 intel/dlstreamer:2025.0.1.2-ubuntu22
cd /workspace && python3 app.py

 Metadata Example (meta.json)
-------------------------------
[
  {
    "frame_id": 42,
    "objects": [
      {
        "label": "person",
        "confidence": 0.98,
        "attributes": {
          "gender": "male",
          "glasses": "yes"
        }
      }
    ]
  }
]

 Benchmarking
----------------
Use benchmark_app inside the container:
benchmark_app -m models/person-detection-0200.xml -d CPU -hint none -nireq 2 -nstreams 2

 Credits
----------
- Intel® DL Streamer
- OpenVINO™ Toolkit
- Flask

