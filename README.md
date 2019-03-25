# Poor man's Rekognition

Open source alternative to Amazon Rekognition offered by AWS. Currently, can identify 1091 clebrity faces.  
Uses deep metric learning instead of deep learning for face identificaton.

## Quick setup

1. create virtual env, install requirements
2. Run flask server (`python driver.py`)
3. This is a REST application. Fire up POSTMAN

### Route descriptions

```
POST /recogniseFaces
```

(Set form type to be form-data)  
params::

`"image": (The__image_file)` [Choose 'file' in the drop down that appears besides the key input field][or]  
`"video": (The_video_file)` [Attach the video file]

(Note): If both parameters are set, only the image is processed.

Return values:  
In case of an image, a JSON string will likeliness of each face is returned.  
In case of a video, a JSON string indicating the result is returned.

```
GET /recogniseFaces
```

(Returns the latest saved image/video)  
params::

`"image"` : If image parameter is set, then the latest processed image is returned.  
 [OR]  
`"video"` : If video parameter is set, then the latest processed video is returned.

(Note): If both parameters are set, only the image is returned.
This returns the processed image.(A label for each bounded box for each face. The descriptions of the label are returned through the post request).

```
GET  /names
```

(no params)

Return values: A JSON string with the names of all celebrities that can be recognised

```
POST /feedback
```

(Lets you tune the model with your feedback)  
params::

`"image" : (The_image_file)` [Choose 'file' in the drop down that appears besides the key input field. Put body type to be Form-data]  
`"name" : (A String that has underscores instead of spaces and all small)` [This is the name that you want the model to understand, as the person in the pic](Note): Make sure you get the names of all people first before using this route. That will help you fine tune already existing celebrity faces.The model will predict with less confidence next time. The more images you give of a single person, the more the confidence turns in your favour.

Return value: A JSON string indicating success or failure

dataset accumulated using my [image scraping tool](https://github.com/gigatesseract/GImageScrape)
link to dataset: [here](https://drive.google.com/open?id=1NpuNBH6FNwPTXpxxPZ-xbqh3YhowcbF5)
link to input/output files: [here](https://drive.google.com/open?id=1n7_gZiYdT1nfJMj-oUqMKrORQtMCle1v)

###### Can recognise 1081 ceberities, trained on 21592 images. (Names are given in known_celebrities.txt)

```

```
