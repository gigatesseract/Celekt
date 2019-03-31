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
import recognize_faces as rec_image
from flask import request
import encode_faces
from werkzeug.utils import secure_filename
from werkzeug.wrappers import Response
import json
import os
import pickle


app = Flask(__name__, static_folder="poormanrekog")
CORS(
    app,
    support_credentials=True,
    allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Origin"],
)
api = Api(app)
app.encoding_file = "encodings2.pickle"


if not os.path.exists("static/output"):
    os.makedirs("static/output")

if not os.path.exists("static/output/images"):
    os.makedirs("static/output/images")


if not os.path.exists("static/output/videos"):
    os.makedirs("static/output/videos")


class recData(Resource):
    def post(self):  # processed the image/video and returns appropriate json

        if "image" in request.files:
            image = request.files["image"]
            coordinates, dict = rec_image.recognise_faces(app.encoding_file, image)
            data = {}
            for (i, value) in enumerate(dict):
                data[str(i)] = value

            return jsonify(
                {
                    "success": "image processed successfully.",
                    "likeliness": dict,
                    "coordinates": coordinates,
                }
            )

        elif "video" in request.files:
            print("else statment")
            f = request.files["video"]

            f.save(secure_filename(f.filename))
            rec_image.recognise_video(
                app.encoding_file, f.filename, "static/output/videos/processed.mp4"
            )
            os.remove(f.filename)

            return jsonify(
                {
                    "success": "Video processed and saved successfully. Hit a get request to get it"
                }
            )

    def get(self):
        # returns the last saved video
        if os.path.isfile("static/output/videos/processed.mp4"):
            # g = wrap_file("static/output/videos/processed.mp4")
            # return Response(g, direct_passthrough=True)
            return make_response(
                send_file(
                    "static/output/videos/processed.mp4",
                    attachment_filename="processed.mp4",
                ),
                200,
            )

        else:
            return jsonify({"error": "No latest video found. Create one!"})


class feedBack(Resource):
    def post(self):

        # gets an image and its corresponsing label and adds it to encodings
        if "image" not in request.files:
            return jsonify({"error": "Supply an 'image' file and a 'name'"})

        if "name" not in request.form:
            return jsonify(
                {
                    "name_error": "Enter a valid name. A valid name has underscores instead of spaces. Make sure you get the list of all celebrities so there isn't two names for the single person."
                }
            )
        else:
            name = request.form["name"]
            image = request.files["image"]
            encode_faces.feedback(app.encoding_file, image, name)
            return jsonify({"success": "name added successfully"})


class listNames(Resource):
    # lists all names of known celebrities

    def get(self):

        data = pickle.loads(open(app.encoding_file, "rb").read())
        names = list(set(data["names"]))
        print(len(names))
        return jsonify({"success": "Names received successfully", "names": names})


class findSimilarity(Resource):
    def post(self):
        if "image1" not in request.files or "image2" not in request.files:
            return jsonify(
                {
                    "error": "Send two images with keys 'image1' and 'image2' respectively"
                }
            )
        else:
            img1 = request.files["image1"]
            img2 = request.files["image2"]
            sim = rec_image.similarity(img1, img2)
            return jsonify({"similarity": sim})


class timeFaces(Resource):
    def post(self):
        # post request will return a json about which celebrity is there from which second to which second. Right now, it will return celebrity faces in every frame

        if "video" not in request.files:
            return jsonify({"error": "Send a video"})
        else:
            f = request.files["video"]
            f.save(secure_filename(f.filename))
            processed_json = rec_image.json_from_faces(app.encoding_file, f.filename)
            os.remove(f.filename)

            return jsonify(
                {"processed": processed_json, "success": "video processed successfully"}
            )


class root(Resource):
    def get(self):
        return make_response(send_file("templates/index.html"))


api.add_resource(recData, "/recogniseFaces")
api.add_resource(feedBack, "/feedback")
api.add_resource(listNames, "/names")
api.add_resource(root, "/")
api.add_resource(findSimilarity, "/similarity")
api.add_resource(timeFaces, "/timeFaces")


if __name__ == "__main__":
    app.run(port=8765, debug=True)
