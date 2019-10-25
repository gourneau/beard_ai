import asyncio, io, glob, os, sys, time, uuid, requests
from urllib.parse import urlparse
from io import BytesIO

from PIL import Image, ImageDraw, ImageTk
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType, FaceAttributeType
import cv2
import jsonpickle
from jinja2 import Environment, FileSystemLoader, Template


# Set the FACE_SUBSCRIPTION_KEY environment variable with your key as the value.
# This key will serve all examples in this document.

KEY = ""

# Set the FACE_ENDPOINT environment variable with the endpoint from your Face service in Azure.
# This endpoint will be used in all examples in this quickstart.
ENDPOINT = "https://westcentralus.api.cognitive.microsoft.com/"

# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

camera = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not camera.isOpened():
    raise IOError("Cannot open webcam")

while 1:
    print("Tick")

    for x in range(20):
        return_value, image = camera.read()
        cv2.imwrite('opencv.jpg', image)
    
    snap = open("opencv.jpg", 'rb')

    detected_faces = face_client.face.detect_with_stream( snap,
        return_face_attributes=list([FaceAttributeType.age, 
                                                            FaceAttributeType.gender,
                                                            FaceAttributeType.head_pose,
                                                            FaceAttributeType.smile,
                                                            FaceAttributeType.facial_hair,
                                                            FaceAttributeType.glasses,
                                                            FaceAttributeType.emotion,
                                                            FaceAttributeType.hair,
                                                            FaceAttributeType.makeup,
                                                            FaceAttributeType.occlusion,
                                                            FaceAttributeType.accessories,
                                                            FaceAttributeType.blur,
                                                            FaceAttributeType.exposure,
                                                            FaceAttributeType.noise])
    )

    if not detected_faces:
        # raise Exception('No face detected from image')
        print("No Face Found!")

    # Convert width height to a point in a rectangle
    def getRectangle(faceDictionary):
        print(faceDictionary.face_attributes.facial_hair)
        print(faceDictionary.face_attributes.emotion)

        rect = faceDictionary.face_rectangle

        left = rect.left
        top = rect.top
        bottom = left + rect.height
        right = top + rect.width
        return ((left, top), (bottom, right))

    img = Image.open(snap)

    # For each face returned use the face rectangle and draw a red box.
    draw = ImageDraw.Draw(img)

    last_face = {}
    last_emo = {}
    for face in detected_faces: 
        draw.rectangle(getRectangle(face), outline='red')
        last_face = jsonpickle.encode(face.face_attributes.facial_hair)
        last_emo =  jsonpickle.encode(face.face_attributes.emotion)

    # Display the image in the users default image browser.
    img.save("ai.jpg")
    with open('tmpl.j2.html') as file_:
        template = Template(file_.read())

        # to save the results
        with open("index.html", "w") as fh:
            fh.write(template.render(ai= last_face , emo = last_emo ))
            
    time.sleep(2)
