from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import os
import tempfile

app = Flask(__name__)
CORS(app)


def build_format(quality):
    if quality == "audio":
        return "bestaudio"
    elif quality == "720":
        return "best[height<=720]"
    elif quality == "1080":
        return "best[height<=1080]"
    return "best"


@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    url = data.get("url")
    quality = data.get("quality", "best")

    if not url:
        return jsonify({"error": "Lien manquant"}), 400

    try:
        temp_dir = tempfile.mkdtemp()

        ydl_opts = {
            "format": build_format(quality),
            "outtmpl": os.path.join(temp_dir, "%(title)s.%(ext)s"),
            "merge_output_format": "mp4",
            "noplaylist": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()
