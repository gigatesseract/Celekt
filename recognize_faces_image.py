import face_recognition
import argparse
import pickle
import cv2
import numpy
from flask import request
from werkzeug.wrappers import Response
import base64


def recognise_faces(encoding_file, image, detection_method="hog"):
    npimg = numpy.fromfile(image, numpy.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    data = pickle.loads(open(encoding_file, "rb").read())

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # detect the (x, y)-coordinates of the bounding boxes corresponding
    # to each face in the input image, then compute the facial embeddings
    # for each face

    boxes = face_recognition.face_locations(rgb, model=detection_method)
    encodings = face_recognition.face_encodings(rgb, boxes)

    # initialize the list of names for each face detected
    names = []

    # loop over the facial embeddings
    for encoding in encodings:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"

        # check to see if we have found a match
        if True in matches:
            # find the indexes of all matched faces then initialize a
            # dictionary to count the total number of times each face
            # was matched
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
                print(name)

            # determine the recognized face with the largest number of
            # votes (note: in the event of an unlikely tie Python will
            # select first entry in the dictionary)

            name = max(counts, key=counts.get)

        # update the list of names
        names.append(name)

    # loop over the recognized faces
    for ((top, right, bottom, left), name) in zip(boxes, names):
        # draw the predicted face name on the image
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(
            image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2
        )

    jpg, b = cv2.imencode(".jpg", image)
    cv2.imwrite("static/images/temp.jpg", image)
    with open("static/images/temp.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string

    # jpg_as_text = base64.b64encode(b)
    # return jpg_as_text


# # show the output image

