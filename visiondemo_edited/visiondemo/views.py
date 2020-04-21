import os
import random
import string
import time
import uuid

from django.shortcuts import render, render_to_response
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
#from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO
from io import StringIO
import numpy as np
import cv2
import requests

from .forms import URLForm, UploadFileForm

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# MAIN PAGE
def index(request):
    return render(request, 'visiondemo/demo.html')  

# RESULT PAGE
def result(request):
    if 'cookie_tag' in request.COOKIES:
        tag = request.COOKIES[ 'cookie_tag' ]
        print('cookie_tag: %s' % (tag))
        input_img_fname = '../media/%s_tmp.jpg' % (tag)
        output_img_fname = '../media/%s_tmp_out.jpg' % (tag)
        return render(request, 'visiondemo/demo.html', {'image_list': [input_img_fname,output_img_fname]})
    else:
        return Http404("Error")


def handle_uploaded_file(f, fname):
    with open(fname, 'wb+') as dst:
        for chunk in f.chunks():
            dst.write(chunk)

def loadFromExternalApp(filepath):
    while not os.path.exists(filepath+'.done'):
        time.sleep(1)
        pass
    print('found result...')
    return 1 #json.load(open(filepath))

def dispatch_job(tag):
    print(BASE_DIR+ 'media/'+ tag)
    open(os.path.join(BASE_DIR, 'media/', tag+'.query.done'), 'w').close()
    return loadFromExternalApp(os.path.join(BASE_DIR, 'media/', tag+'.result'))

def lineDrawing(img):
    kernel = np.array([
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        ], np.uint8)
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    dilated = cv2.dilate(grey, kernel, iterations=1)
    diff = cv2.absdiff(dilated, grey)
    contour = 255 - diff
    return contour

def process(tag, f):
    #img = Image.open(uploadfile)
    fname = f
    img = cv2.imread(fname)
    #img_contour = img.convert('L')
    img_contour = lineDrawing(img)
    print('fa')
    #img_bytes = BytesIO()
    fname = os.path.join(BASE_DIR, 'media\%s_tmp_out.jpg' % (tag))
    #img_contour.save(img_bytes, format='PNG')
    #imafe = InMemoryUploadedFile(
    #    file=img_bytes,
    #    field_name='image',
    #    name='%s_tmp_out.jpg' % (tag),
    #    content_type=uploadfile.content_type,
    #    size=uploadfile.size,
    #    charset=None)
    print(fname)
    cv2.imwrite(fname, img_contour)
    return img_contour

# HANDLE FILE UPLOAD
@csrf_exempt
def fileupload(request):

    N = 10
    tag = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
    tag = str(uuid.uuid4())
    fname = os.path.join(BASE_DIR, 'media\%s_tmp.jpg' % (tag))
    print('fileupload tag: %s' % (tag))
    print(fname)

    response = HttpResponseRedirect(reverse('visiondemo:result'))
    response.set_cookie( 'cookie_tag', tag )


    if request.method == 'POST':
        # FROM DROPZONE UPLOAD
        try:
            print('try UploadFileForm ...')
            print('form')
            form = UploadFileForm(request.POST, request.FILES)
            print(str(form.is_valid()))
            if form.is_valid():
                handle_uploaded_file(request.FILES['file'], fname)
                print('Upload succeeded.')
                #dispatch_job(tag)
                uploadfile = request.FILES['file']
                img = process(tag, fname)
                return response
        except:
            pass
        # FROM URL TEXT
        try:
            print('URL form...')
            form = URLForm(request.POST)
            print(str(form.is_valid()))
            if form.is_valid():
                print(form.cleaned_data['myinput'])
                url = form.cleaned_data['myinput']
                session = requests.session()
                image = session.get(url)
                img_contour = Image.open(BytesIO(image.content))
                img_bytes = BytesIO()
                img_contour.save(img_bytes, format='PNG')
                imafe = InMemoryUploadedFile(
                    file=img_bytes,
                    field_name='image',
                    name='%s_tmp_out.jpg' % (tag),
                    content_type=img_contour.format,
                    size=img_contour.size,
                    charset=None)
                print('Download succeeded.')
                handle_uploaded_file(imafe, fname)
                img = process(tag, fname)
                #dispatch_job(tag)
                return response
        except:
            pass
    print('Error')
    return Http404("Error")

