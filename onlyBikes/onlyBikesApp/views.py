from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import BikeModel
from django.template import loader
from django.urls import reverse
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render, redirect
from django.urls import reverse
from twilio.rest import Client
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required 
from . models import User
from .utils.utils import test_data
from os import environ
import cv2 
import numpy as np
from matplotlib import pyplot as plt
import os
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util
import matplotlib

from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import threading
###############################################################################################


# Auth0 Section
oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.SOCIAL_AUTH_AUTH0_KEY,
    client_secret=settings.SOCIAL_AUTH_AUTH0_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.SOCIAL_AUTH_AUTH0_DOMAIN}/.well-known/openid-configuration",
)

def login(request):
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )
    
def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token
    return redirect(request.build_absolute_uri(reverse("index")))


@login_required
def logout(request):
    django_logout(request)
    domain = settings.SOCIAL_AUTH_AUTH0_DOMAIN
    client_id = settings.SOCIAL_AUTH_AUTH0_KEY
    return_to = 'http://127.0.0.1:8000' # this can be current domain
    return redirect(f'https://{domain}/v2/logout?client_id={client_id}&returnTo={return_to}')


###############################################################################################    

# TWILIO CUSTOMIZATION

twilio_sid = settings.TWILIO_SID
twilio_auth = settings.TWILIO_AUTH
client = Client(twilio_sid,twilio_auth)

def testmessage():
    message = client.messages.create(
    body='ザワルドときをとまれ',
    from_='+18563866349',
    to='+18187978710'
    )

    # print(message.sid)

############################################################################################### 

# Everything Else

def index(request):
    BikeModel.objects.all().delete()
    all_bikes = BikeModel.objects.all()
    
    # Note: Remove this in production
    if len(all_bikes) < 7:
        all_bikes = test_data()
        for bike in all_bikes: 
            bike.save()


    return render(request, "index.html", {"all_bikes" : all_bikes})

def home(request):
    return render(request, 'home.html')

def temp(request):
    return render(request, 'temp.html')

def show(request, id):
    bike = BikeModel.objects.filter(id=id)

    if len(bike) == 0:
        return redirect('/index')
    return render(request, 'show.html', {"bike" : bike[0]})

def contact(request):
    return render(request, 'contact.html')

def leaderboard(request):
    query_object = BikeModel.objects.all() 
    rescued_loc = []
    
    if len(query_object) > 0:
        for bike in query_object:
            rescued_loc.append([bike.rescued_long, bike.rescued_lat])

    return render(request, 'leaderboard.html', {
        "mapbox_token" : environ["MAPBOX_TOKEN"],
        "rescued_loc" : rescued_loc
        })

# -- Utility Functions --

def add(request):
    template = loader.get_template('onlyBikesApp/add.html')
    return HttpResponse(template.render({}, request))

def addbike(request):
    brand = request.POST['brand']
    model = request.POST['model']
    price = request.POST['price']
    condition = request.POST['condition']
    location = request.POST['location']
    description = request.POST['description']
    
    bike = BikeModel.objects.create(brand = brand, model = model, price = price, condition = condition, location = location, description = description)
    bike.save()

    return HttpResponseRedirect(reverse('test_view'))

    # return HttpResponse(html, status = 200)

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def update_profile(request):
    username = request.user
    first = request.POST['first']
    last = request.POST['last']
    email = request.POST['email']
    phone = request.POST['phone']
    bio = request.POST['bio']
    user = User.objects.get(username = username)
    # print(request.POST)
    user.first_name = first
    # print(user.last_name, last)
    user.last_name = last
    user.email = email
    user.phone_number = phone
    # print(user.bio, bio)
    user.bio = bio
    user.save()
    return HttpResponseRedirect(reverse('profile'))










#############################################################################################


MODEL_NAME = 'ssd_mobilenet_fpn_lite'
PRETRAINED_MODEL_NAME = 'ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8'
LABEL_MAP_NAME = 'label_map.pbtxt'

paths = {
    

    'ANNOTATION_PATH': os.path.join('../annotation'),
    'IMAGE_PATH': os.path.join('../onlyBikes', 'media'),
    'MODEL_PATH': os.path.join('../tensormodel'),
    'CHECKPOINT_PATH': os.path.join('../tensormodel',MODEL_NAME), 
}


files = {
    'PIPELINE_CONFIG':os.path.join('../tensormodel', MODEL_NAME, 'pipeline.config'),
    'LABELMAP': os.path.join(paths['ANNOTATION_PATH'], LABEL_MAP_NAME)
}




configs = config_util.get_configs_from_pipeline_file(files['PIPELINE_CONFIG'])
detection_model = model_builder.build(model_config=configs['model'], is_training=False)

# Restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(os.path.join(paths['CHECKPOINT_PATH'], 'ckpt-102')).expect_partial()

@tf.function
def detect_fn(image):
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections

category_index = label_map_util.create_category_index_from_labelmap(files['LABELMAP'])
IMAGE_PATH = os.path.join(paths['IMAGE_PATH'], 'test', 'unknown.png')


@gzip.gzip_page
def cam(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass
    return render(request, 'cam.html')

#to capture video class
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()
            

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        cap = self.video
        (self.grabbed, self.frame) = cap.read()
        ret, frame = cap.read()
        image_np = np.array(frame)
        
        input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
        detections = detect_fn(input_tensor)
        
        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy()
                    for key, value in detections.items()}
        detections['num_detections'] = num_detections

        # detection_classes should be ints.
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

        label_id_offset = 1
        image_np_with_detections = image_np.copy()

        viz_utils.visualize_boxes_and_labels_on_image_array(
                    image_np_with_detections,
                    detections['detection_boxes'],
                    detections['detection_classes']+label_id_offset,
                    detections['detection_scores'],
                    category_index,
                    use_normalized_coordinates=True,
                    max_boxes_to_draw=5,
                    min_score_thresh=0.35,
                    agnostic_mode=False)

        ret, jpeg = cv2.imencode('.jpg', image_np_with_detections)
        return jpeg.tobytes()

    def update(self):
        while True:
            cap = self.video
            (self.grabbed, self.frame) = cap.read()
            ret, frame = cap.read()
            image_np = np.array(frame)
            
            input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
            detections = detect_fn(input_tensor)
            
            num_detections = int(detections.pop('num_detections'))
            detections = {key: value[0, :num_detections].numpy()
                        for key, value in detections.items()}
            detections['num_detections'] = num_detections

            # detection_classes should be ints.
            detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

            label_id_offset = 1
            image_np_with_detections = image_np.copy()

            viz_utils.visualize_boxes_and_labels_on_image_array(
                        image_np_with_detections,
                        detections['detection_boxes'],
                        detections['detection_classes']+label_id_offset,
                        detections['detection_scores'],
                        category_index,
                        use_normalized_coordinates=True,
                        max_boxes_to_draw=5,
                        min_score_thresh=0.35,
                        agnostic_mode=False)

            # cv2.imshow('object detection',  cv2.resize(image_np_with_detections, (800, 600)))
            



def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
