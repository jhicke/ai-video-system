import json
import subprocess
from pathlib import Path

def load_template(path="template.json"):
    with open(path, "r") as f:
        return json.load(f) 

def render_video(config):
    background = config["background"]
    audio = config["audio"]
    output = config["output"]
    resolution = config["resolution"]
    fps = config["fps"]

    cmd = [
        "ffmpeg",
        "-y",
        "-i", background,
        "-i", audio,
        "-vf", f"scale={resolution}",
        "-r", str(fps),
        "-shortest",
        output
    ]

    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    config = load_template()
    render_video(config)
    print(f"Video rendered successfully: {config['output']}")