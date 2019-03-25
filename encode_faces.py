from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os


def encode(dataset_path, encoding_file, detection_method="hog"):

    # grab the paths to the input images in our dataset
    print("[INFO] quantifying faces...")
    imagePaths = list(paths.list_images(dataset_path))
    knownEncodings = []
    knownNames = []

    # loop over the image paths
    for (i, imagePath) in enumerate(imagePaths):
        # extract the person name from the image path
        if i % 2000 == 0:
            print("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)))
        name = imagePath.split(os.path.sep)[-2]

        # load the input image and convert it from RGB (OpenCV ordering)
        # to dlib ordering (RGB)
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # detect the (x, y)-coordinates of the bounding boxes
        # corresponding to each face in the input image
        boxes = face_recognition.face_locations(rgb, model=detection_method)

        # compute the facial embedding for the face
        encodings = face_recognition.face_encodings(rgb, boxes)

        # loop over the encodings
        for encoding in encodings:
            # add each encoding + name to our set of known names and
            # encodings
            knownEncodings.append(encoding)
            knownNames.append(name)

    # dump the facial encodings + names to disk
    print("[INFO] serializing encodings...")
    data = {"encodings": knownEncodings, "names": knownNames}
    f = open(encoding_file, "wb")
    f.write(pickle.dumps(data))
    print("pickle file generated")
    f.close()


def feedback(encoding_file, image_path, name, detection_method="hog"):
    data = pickle.loads(open(encoding_file, "rb").read())
    image = cv2.imread(image_path)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb, model=detection_method)
    encodings = face_recognition.face_encodings(rgb, boxes)

    knownEncodings = data["encodings"]
    knownNames = data["names"]
    for encoding in encodings:
        # add each encoding + name to our set of known names and
        # encodings
        knownEncodings.append(encoding)
        knownNames.append(name)

    f = open(encoding_file, "wb")
    data = {"encodings": knownEncodings, "names": knownNames}
    f.write(pickle.dumps(data))
    print("pickle file modified successfully")


if __name__ == "__main__":
    filename = "enc123.pickle"
    encode("dataset/", filename)

