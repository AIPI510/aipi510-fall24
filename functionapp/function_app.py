import azure.functions as func
import datetime
import json
import logging

import numpy as np    # we're going to use numpy to process input and output data
import onnxruntime    # to inference ONNX models, we use the ONNX Runtime
import onnx
from onnx import numpy_helper
import json
import time

import cv2    
from PIL import Image 

class ResnetClassifier():
    """
    Utility class to implement a resnet50 classifier
    """

    def __init__(self): 
        """
        Initialize an instance of the class
        """
        self.session = onnxruntime.InferenceSession('resnet50v2/resnet50v2.onnx', None)

        with open('imagenet-simple-labels.json') as f:
            data = json.load(f)        
            self.labels = np.asarray(data)

    def preprocess(self, input_data):
        """
        Preprocess an image
        Source: https://github.com/onnx/onnx-docker/blob/master/onnx-ecosystem/inference_demos/resnet50_modelzoo_onnxruntime_inference.ipynb
        """
        # convert the input data into the float32 input
        img_data = input_data.astype('float32')

        #normalize
        mean_vec = np.array([0.485, 0.456, 0.406])
        stddev_vec = np.array([0.229, 0.224, 0.225])
        norm_img_data = np.zeros(img_data.shape).astype('float32')
        for i in range(img_data.shape[0]):
            norm_img_data[i,:,:] = (img_data[i,:,:]/255 - mean_vec[i]) / stddev_vec[i]
            
        #add batch channel
        norm_img_data = norm_img_data.reshape(1, 3, 224, 224).astype('float32')
        return norm_img_data

    def softmax(self, x):
        """
        Implement softmax
        Source: https://github.com/onnx/onnx-docker/blob/master/onnx-ecosystem/inference_demos/resnet50_modelzoo_onnxruntime_inference.ipynb
        """
        x = x.reshape(-1)
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=0)

    def postprocess(self, result):
        return self.softmax(np.array(result)).tolist()

    def scale(self, image): 
        """
        Scale to a resolution suitable for resnet ... note the laziness here, we 
        force everything to fit into 224x224 pixels to satisfy resnet input dimensions. 
        """
        array = np.array(image) 
        scaled = cv2.resize(array, (224, 224), interpolation=cv2.INTER_CUBIC) 
        
        # Smooth to reduce artifacts from scaling
        blurred = cv2.blur(scaled, (2,2))
        
        return Image.fromarray(blurred) 

    def classify(self, image): 
        """
        Classify an image w/ resnet50
        """
        image_data = np.array(image).transpose(2, 0, 1)
        input_data = self.preprocess(image_data)

        input_name = self.session.get_inputs()[0].name

        start = time.time()
        raw_result = self.session.run([], {input_name: input_data})
        end = time.time()
        res = self.postprocess(raw_result)

        inference_time = np.round((end - start) * 1000, 2)
        idx = np.argmax(res)

        print('Final top prediction is: ' + self.labels[idx])
        print('Inference time: ' + str(inference_time) + " ms")
    
        sort_idx = np.flip(np.squeeze(np.argsort(res)))
        print('Top 5 labels: ' + self.labels[sort_idx[:5]])

        return(self.labels[idx])

app = func.FunctionApp()

@app.route(route="TrackstarsHttp", auth_level=func.AuthLevel.ANONYMOUS)
def TrackstarsHttp(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')    

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        classifier = ResnetClassifier()

        image = Image.open('images/dog.jpg')
        label = classifier.classify(classifier.scale(image))
        return func.HttpResponse(f"Hello, {name}! The predicted label for the image is {label}.")
        
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )