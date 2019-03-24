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


app = Flask(__name__)
CORS(
    app,
    support_credentials=True,
    allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Origin"],
)
api = Api(app)


class recData(Resource):
    def post(self):

        if "image" in request.form:
            image = request.files["image"]
            dict = rec_image.recognise_faces("encodings2.pickle", image)
            data = {}
            for (i, value) in enumerate(dict):
                data[str(i)] = value

            return Response(json.dumps(data), mimetype="application/json")

            if "download" in request.form:
                # return send_file(
                #     "static/images/temp.jpg", attachment_filename="faces.jpg"
                # )
                return make_response(
                    send_file(
                        "static/images/temp.jpg", attachment_filename="faces.jpg"
                    ),
                    200,
                )

            # return (
            #     send_from_directory(
            #         "static/images/",
            #         "temp.jpg",
            #         as_attachment=True,
            #         mimetype="image/jpg",
            #         attachment_filename="temp.jpg",
            #     ),
            # )
            # return response
        elif "video" in request.form:
            f = request.files["video"]
            f.save(secure_filename(f.filename))
            rf.recognise_video(
                "encodings2.pickle", f.filename, "static/images/" + f.filename
            )

            return make_response(
                send_file(
                    "static/images/" + f.filename, attachment_filename="video.mp4"
                )
            )


class sendData(Resource):
    def get(self):
        return make_response(
            send_file("static/images/temp.jpg", attachment_filename="faces.jpg"), 200
        )


api.add_resource(recData, "/recogniseData")
api.add_resource(sendData, "/sendData")


if __name__ == "__main__":
    app.run(debug=True)
