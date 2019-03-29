from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os
import numpy


def encode(dataset_path, encoding_file, detection_method="hog"):

    imagePaths = list(paths.list_images(dataset_path))
    encodings = []
    names = []

    for (i, imagePath) in enumerate(imagePaths):

        name = imagePath.split(os.path.sep)[-2]
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model=detection_method)
        encodings = face_recognition.face_encodings(rgb, boxes)
        for encoding in encodings:
            knownEncodings.append(encoding)
            knownNames.append(name)

    encoded_data = {"encodings": encodings, "names": names}
    f = open(encoding_file, "wb")
    f.write(pickle.dumps(encoded_data))
    f.close()


def feedback(encoding_file, image, name, detection_method="hog"):
    # basically get the encoded file, append the encodings of given image and write it to the same file.
    encoded_data = pickle.loads(open(encoding_file, "rb").read())
    image = cv2.imdecode(numpy.fromfile(image, numpy.uint8), cv2.IMREAD_COLOR)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb, model=detection_method)
    encodings = face_recognition.face_encodings(rgb, boxes)

    encodings = encoded_data["encodings"]
    names = encoded_data["names"]
    for encoding in encodings:

        encodings.append(encoding)
        names.append(name)

    f = open(encoding_file, "wb")
    data = {"encodings": encodings, "names": names}
    f.write(pickle.dumps(data))
    f.close()


if __name__ == "__main__":
    filename = "enc123.pickle"
    encode("dataset/", filename)

