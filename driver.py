from flask import Flask, render_template, jsonify, send_from_directory, send_file
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from flask_restful.utils import cors
import recognize_faces_image as rec_image
from flask import request
import encode_faces


app = Flask(__name__)
CORS(
    app,
    support_credentials=True,
    allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Origin"],
)
api = Api(app)


class recImage(Resource):
    def post(self):

        image = request.files["image"]
        (img_string, dict) = rec_image.recognise_faces("enc.pickle", image)
        response = jsonify({"key": img_string.decode("utf-8"), "dict": dict})

        # return (
        #     send_from_directory(
        #         "static/images/",
        #         "temp.jpg",
        #         as_attachment=True,
        #         mimetype="image/jpg",
        #         attachment_filename="temp.jpg",
        #     ),
        # )
        return response


api.add_resource(recImage, "/recognise")


if __name__ == "__main__":
    app.run(debug=True)
