# Poor man's Rekognition

Open source alternative to Amazon Rekognition offered by AWS. Currently, can identify 1081 clebrity faces.  
Uses deep metric learning instead of deep learning for face identificaton.

## Quick setup

1. create virtual env, install requirements
2. Run flask server (`python driver.py`)
3. Go to root route

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
In case of an image, a JSON string will likeliness of each face, and the bounding box for each face are returned.  
In case of a video, a JSON string indicating the result is returned.

In case of an image:

```
"likeliness": [An array of names for each face],
"coordinates":{"top": number,
                "bottom": number,
                "left": number,
                "right":number}
"success" : "image processed successfully"

```

In case of video:

```
"success": "Video processed and saved successfully. Hit a get request to get it"
```

```
GET /recogniseFaces
```

(Returns the latest saved video - as a resource)  
(no params)

```
GET  /names
```

(no params)

Return values:

```
"success": "Names received successfully"
"names": [Array of values]

```

```
POST /feedback
```

(Lets you tune the model with your feedback)  
params::

`"image" : (The_image_file)` [Choose 'file' in the drop down that appears besides the key input field. Put body type to be Form-data]  
`"name" : (A String that has underscores instead of spaces and all small)`  
 (This is the name that you want the model to understand, as the person in the pic)

(Note): Make sure you get the names of all people first before using the get route. That will help you fine tune already existing celebrity faces.  
The model will predict with less confidence next time. The more images you give of a single person, the more the confidence turns in your favour.

Return value:

```
"success": "name added successfully"})


```

```
POST /timeFaces
```

(Gives the presence of celebrities in seconds, whenever they are present)

```
"video": (The video file)
```

Return JSON:

```
{
"processed":[
  {"timestamp A to timestamp B": "name of celebrity},
  {"timestamp C to timestamp D": "name of celebrity}....
],
  "success":"video processed successfully"

}
```

dataset accumulated using my [image scraping tool](https://github.com/gigatesseract/GImageScrape)  
link to dataset: [here](https://drive.google.com/open?id=1NpuNBH6FNwPTXpxxPZ-xbqh3YhowcbF5)  
link to input/output files: [here](https://drive.google.com/open?id=1n7_gZiYdT1nfJMj-oUqMKrORQtMCle1v)

###### Can recognise 1077 ceberities, trained on 21592 images. (Names are given in known_celebrities.txt)

Have fun! :smiley: :smiley: :smiley:
