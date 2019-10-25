# beard_ai

A beard ai script .

## Conda env

Install conda if you don't have it. https://www.anaconda.com/distribution/

Once you have conda make a env
```
conda create --name beard --file conda.list
```
Then activate it 

```
conda activate beard
```


## Azure API

This is built using the Azure API. You will need to get a free key from here

https://azure.microsoft.com/en-us/services/cognitive-services/face/


Get the key and fill in this, also change the URL if it has changed. (The full url listed on their page won't work something like the one listed below)

```
KEY = ""
ENDPOINT = "https://westcentralus.api.cognitive.microsoft.com/"
```

Then you can run 

```
python face.py
```

it will create a file named index.html you can view in a browser
