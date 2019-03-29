import face_recognition
import argparse
import pickle
import cv2
import numpy
from flask import request
from werkzeug.wrappers import Response
import base64
from collections import Counter
import imutils


def recognise_faces(encoding_file, image, detection_method="hog"):
    image = cv2.imdecode(numpy.fromfile(image, numpy.uint8), cv2.IMREAD_COLOR)
    encoded_vectors = pickle.loads(open(encoding_file, "rb").read())
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    bounding_boxes = face_recognition.face_locations(rgb, model=detection_method)
    encodings = face_recognition.face_encodings(rgb, bounding_boxes)

    names = []
    counter_dict = []
    coordinates = []

    for encoding in encodings:
        matches = face_recognition.compare_faces(
            encoded_vectors["encodings"], encoding, 0.6
        )
        name = "Unknown"

        if True in matches:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            names_dict = Counter()

            for i in matchedIdxs:
                name = encoded_vectors["names"][i]
                names_dict[name] += 1

            temp_dict = []
            s = 0
            names_dict = dict(names_dict.most_common(3))

            s = sum(names_dict.values())
            for key in names_dict.keys():
                names_dict[key] = names_dict[key] / s
            for (key, value) in names_dict.items():

                temp_dict.append({"name": key, "likeliness": value})

            counter_dict.append(temp_dict)
        names.append(str(len(counter_dict) - 1))

    for ((top, right, bottom, left), name) in zip(bounding_boxes, names):
        coordinates.append({"top": top, "right": right, "bottom": bottom, "left": left})

    return coordinates, counter_dict


def recognise_video(encoding_file, input_path, output_path, detection_method="hog"):
    encoded_data = pickle.loads(open(encoding_file, "rb").read())
    stream = cv2.VideoCapture(input_path)
    writer = None
    while True:
        (grabbed, frame) = stream.read()
        if not grabbed:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb = imutils.resize(frame, width=500)
        r = frame.shape[1] / float(rgb.shape[1])

        boxes = face_recognition.face_locations(rgb, model=detection_method)
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []

        for encoding in encodings:

            matches = face_recognition.compare_faces(
                encoded_data["encodings"], encoding
            )

            if True in matches:

                true_indices = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                for i in true_indices:

                    name = encoded_data["names"][i]

                    if not name in counts:
                        counts[name] = 1
                    else:
                        counts[name] += 1
                m = 0
                for key in counts.keys():
                    if counts[key] > m:
                        name = key

            else:
                name = "unknown"

            names.append(name)

        for ((top, right, bottom, left), name) in zip(boxes, names):
            # print("writing frame at " + output_path)

            top = int(top * r)
            right = int(right * r)
            bottom = int(bottom * r)
            left = int(left * r)
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(
                frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2
            )

        if writer is None and output_path is not None:
            print("writing frame at " + output_path)
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            writer = cv2.VideoWriter(
                output_path, fourcc, 24, (frame.shape[1], frame.shape[0]), True
            )

        if writer is not None:
            writer.write(frame)

    stream.release()
    if writer is not None:
        writer.release()

