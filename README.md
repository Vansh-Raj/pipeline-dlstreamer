# DL Streamer Flask Web App
Demo Video: https://youtu.be/XXUsDnoPa54

A lightweight Flask web application using Intel DL Streamer and OpenVINO Toolkit to perform real-time person detection and attribute classification on uploaded videos.

It outputs:
- Annotated video (`output.mp4`) with visual overlays
- Frame-wise metadata (`meta.json`) with labels, confidence scores, and attributes

---

## Features

- Upload videos directly via browser
- Uses Intel pre-trained models to:
  - Detect people (`person-detection-0200`)
  - Classify attributes (`person-attributes-recognition-crossroad-0234`)
- Downloadable results:
  - `output.mp4` with bounding boxes and labels
  - `meta.json` with per-frame detections

---

## Models Used

| Task           | Model Name                                     | Format             |
|----------------|------------------------------------------------|--------------------|
| Detection      | person-detection-0200                          | OpenVINO IR (FP16) |
| Classification | person-attributes-recognition-crossroad-0234  | OpenVINO IR (FP16) |

> Place all model `.xml` and `.bin` files in the `models/` folder.

---

## Project Structure

```text
dlstreamer-webapp/
├── app.py                        # Flask backend
├── requirements.txt              # Python dependencies
├── models/                       # OpenVINO models
│   ├── person-detection-0200.{xml, bin}
│   └── person-attributes-recognition-crossroad-0234.{xml, bin}
├── static/                       # Generated output
│   ├── output.mp4
│   └── meta.json
├── uploads/                      # Uploaded video files
├── templates/
│   └── index.html                # Upload page
└── README.md                     # Project documentation
```

---

## Getting Started

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python3 app.py
```

Then open: [http://localhost:5000](http://localhost:5000)

---

## Docker Support (Optional)

Using Intel DL Streamer Docker image:

```bash
docker run -it -v $PWD:/workspace -p 5000:5000 intel/dlstreamer:2025.0.1.2-ubuntu22
cd /workspace && python3 app.py
```

---

## Sample Metadata (`meta.json`)

```json
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
```

---

## Benchmarking

Run this inside the container or OpenVINO environment:

```bash
benchmark_app -m models/person-detection-0200.xml -d CPU -hint none -nireq 2 -nstreams 2
```

---

## Acknowledgments

- Intel DL Streamer
- OpenVINO Toolkit
- Flask Framework

---

## Sample Output

![Screenshot from 2025-07-02 02-02-48](https://github.com/user-attachments/assets/22f52d2e-a885-40e1-966f-caf708a17f27)
