# Celekt

Open source alternative to Poor Man's Rekognition offered by AWS. Currently, can identify 1091 clebrity faces.  
Uses deep metric learning instead of deep learning for face identificaton.

## Quick setup

1. create virtual env, install requirements
2. Run flask server (`python driver.py`)
3. This is a REST application. Fire up POSTMAN

### Route descriptions

`POST /recData` (Set form type to be form-data)

```
"image" : "True" (Or any string. This acts as a flag for the image identification algorithm)
"image"(this is a file) : (The_file)
```

Note, in case of a video, replace the keys by "video" and attach a sutable video

Return values:  
In case of an image, a JSON string will likeliness of each face is returned.  
In case of a video, the processed video is returned.

`GET /sendFile`  
This returns the processed image.(A label for each bounded box for each face. The descriptions of the label are returned through the above post request) Call this route after posting an image through `/redData`

dataset accumulated using my [image scraping tool](https://github.com/gigatesseract/GImageScrape)

###### Can recognise 1091 ceberities, trained on 22673 images. (Names are given in known_celebrities.txt)
