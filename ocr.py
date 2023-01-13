import io
import os
import json
import base64
import jmespath
from google.cloud import vision
from google.cloud.vision import AnnotateImageResponse

# Instantiates a client
client = vision.ImageAnnotatorClient()

def ocr(path):
    # The name of the image file to annotate
    file_name = os.path.abspath(path)

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()


    ## Performs label detection on the image file
    response = client.annotate_image({
    'image': {'content': base64.b64encode(content).decode('utf-8')},
    'features': [{'type_': vision.Feature.Type.DOCUMENT_TEXT_DETECTION }]
    })

    annotations =  json.loads(AnnotateImageResponse.to_json(response))
    annotations = annotations['textAnnotations'][1::]
    
    # Organizamos los datos con jmespath
    expression = '[].{"word":description, "vert": [[boundingPoly.vertices[0].x, boundingPoly.vertices[0].y], [boundingPoly.vertices[2].x, boundingPoly.vertices[2].y]]}'
    annotations = jmespath.search(expression=expression, data=annotations)
    
    return annotations
