from flask import (
    Flask,
    render_template,
    jsonify,
    send_from_directory,
    send_file,
    make_response,
)
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from flask_restful.utils import cors
import recognize_faces_image as rec_image
from flask import request
import encode_faces
from werkzeug.utils import secure_filename
import recognize_faces_video_file as rf
from werkzeug.wrappers import Response
import json
import os


app = Flask(__name__)
CORS(
    app,
    support_credentials=True,
    allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Origin"],
)
api = Api(app)


if not os.path.exists("static/output"):
    os.makedirs("static/output")

if not os.path.exists("static/output/images"):
    os.makedirs("static/output/images")


if not os.path.exists("static/output/videos"):
    os.makedirs("static/output/videos")


class recData(Resource):
    def post(self):  # processed the image/video, saves it and returns appropriate json

        if "image" in request.files:
            image = request.files["image"]
            dict = rec_image.recognise_faces(
                "encodings2.pickle", image, "static/output/images/temp.jpg"
            )
            data = {}
            for (i, value) in enumerate(dict):
                data[str(i)] = value

            return jsonify(data)

        elif "video" in request.files:
            f = request.files["video"]

            f.save(secure_filename(f.filename))
            rf.recognise_video(
                "encodings2.pickle", f.filename, "static/output/videos/processed.mp4"
            )
            return jsonify(
                {
                    "result": "Video processed and saved successfully. Hit a get request to get it"
                }
            )

    def get(self):
        # returns the last saved file/image (appropriate get parameters required)
        if "image" in request.args:
            if os.path.isfile("static/output/images/temp.jpg"):
                return make_response(
                    send_file(
                        "static/images/temp.jpg", attachment_filename="faces.jpg"
                    ),
                    200,
                )
            else:
                return jsonify({"result": "No latest image found. Create one!"})
        elif "video" in request.args:

            if os.path.isfile("static/output/videos/processed.mp4"):
                return make_response(
                    send_file(
                        "static/output/videos/processed.mp4",
                        attachment_filename="processed.mp4",
                    ),
                    200,
                )

            else:
                return jsonify({"result": "No latest video found. Create one!"})
        else:
            return jsonify({"result": "Request either an audio or video"})


api.add_resource(recData, "/recogniseFaces")


if __name__ == "__main__":
    app.run(debug=True)
