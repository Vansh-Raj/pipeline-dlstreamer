from flask import Flask, render_template, request, send_from_directory
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "static"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        f = request.files["video"]
        input_path = os.path.join(UPLOAD_FOLDER, f.filename)
        output_path = os.path.join(OUTPUT_FOLDER, "output.mp4")
        f.save(input_path)

        # GStreamer pipeline using new efficient models
        command = f"""
        gst-launch-1.0 filesrc location="{input_path}" ! decodebin ! videoconvert ! \
        gvadetect model=models/person-detection-0200.xml device=CPU batch-size=1 nireq=2 ! \
        gvaclassify model=models/person-attributes-recognition-crossroad-0234.xml device=CPU batch-size=1 nireq=2 ! \
        gvawatermark ! videoconvert ! x264enc ! mp4mux ! filesink location="{output_path}"
        """
        subprocess.call(command, shell=True)

        return render_template("index.html", processed=True)

    return render_template("index.html", processed=False)

@app.route("/output")
def output():
    return send_from_directory(OUTPUT_FOLDER, "output.mp4")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)