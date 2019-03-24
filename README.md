# Celekt

Open source alternative to Poor Man's Rekognition offered by AWS. Currently, can identify 1091 clebrity faces.  
Uses deep metric learning instead of deep learning for face identificaton.

## Quick setup

1. create virtual env, install requirements
2. Run flask server (`python driver.py`)
3. This is a REST application. Fire up POSTMAN

### Route descriptions

`POST /recogniseFaces` (Set form type to be form-data)

```
"image": (The_file)    [Choose 'file' in the drop down that appears besides the key input field]
```

```
"video": (The_video_file)   [Attach the video file]
```

(Note): If both parameters are set, only the image is processed.

Return values:  
In case of an image, a JSON string will likeliness of each face is returned.  
In case of a video, a JSON string indicating the result is returned.

`GET /recogniseFaces` (Returns the latest saved image/video)  
params::  
`"image"` : If image parameter is set, then the latest processed image is returned.  
`"video"` : If video parameter is set, then the latest processed video is returned.

(Note): If both parameters are set, only the image is returned.
This returns the processed image.(A label for each bounded box for each face. The descriptions of the label are returned through the post request).

dataset accumulated using my [image scraping tool](https://github.com/gigatesseract/GImageScrape)  
link to dataset: [here](https://drive.google.com/open?id=1NpuNBH6FNwPTXpxxPZ-xbqh3YhowcbF5)  
link to input/output files: [here](https://drive.google.com/open?id=1n7_gZiYdT1nfJMj-oUqMKrORQtMCle1v)

###### Can recognise 1091 ceberities, trained on 22673 images. (Names are given in known_celebrities.txt)
