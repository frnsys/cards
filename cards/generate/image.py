import io
import cv2
import json
import base64
import random
import config
import unidecode
import numpy as np
from PIL import Image, ImageFilter
from urllib import request, parse, error
from collections import namedtuple

# https://pixabay.com/api/docs/
image_url = 'https://pixabay.com/api/?key={}&q='.format(config.PIXABAY_API_KEY)

def image(name):
    # First try the entire name as the query
    url = fetch_image(name)
    if url is not None:
        return process_image(url)

    # Otherwise, blend an image from separate queries
    else:
        parts = [fetch_image(p) for p in name.split(' ')]
        parts = [p for p in parts if p is not None]

        if not parts:
            return '#'

        elif len(parts) == 1:
            return process_image(parts[0])

        else:
            parts = random.sample(parts, 2)
            data = blend_images(*parts)
            return 'data:image/jpeg;base64,{}'.format(data)


def process_image(url):
    req = request.Request(url, headers={'User-Agent': 'Chrome'})
    resp = request.urlopen(req)
    data = io.BytesIO(resp.read())
    img = Image.open(data)
    cimg = find_contours(img)
    img = Image.composite(img, cimg, cimg.convert('L'))

    buff = io.BytesIO()
    img.convert('RGB').save(buff, format='jpeg')
    data = base64.b64encode(buff.getvalue()).decode('utf8')

    return 'data:image/jpeg;base64,{}'.format(data)


def fetch_image(name):
    name = unidecode.unidecode(name)
    q = parse.quote(name.replace(' ', '+'))
    q = name.replace(' ', '+')
    url = image_url + q
    req = request.Request(url, headers={'User-Agent': 'Chrome'})
    resp = request.urlopen(req)
    body = resp.read()
    results = json.loads(body.decode('utf-8'))['hits']

    # Try results until we get an available image
    while results:
        url = results.pop()['webformatURL']
        req = request.Request(url, headers={'User-Agent': 'Chrome'})
        try:
            resp = request.urlopen(req)
            return url
        except error.HTTPError:
            continue


def blend_images(url1, url2):
    # TO DO clean this up
    Point = namedtuple('Point', ['x', 'y'])

    images = []
    for url in [url1, url2]:
        req = request.Request(url, headers={'User-Agent': 'Chrome'})
        resp = request.urlopen(req)
        data = io.BytesIO(resp.read())
        img = Image.open(data)
        images.append(img)

    cimages = []
    for img in images:
        size = Point(*img.size)
        target_size = Point(400, 250)

        # Scale as needed
        x_scale = target_size.x/size.x
        y_scale = target_size.y/size.y
        scale_factor = max(x_scale, y_scale)
        scaled_size = Point(*[int(d*scale_factor) for d in size])
        img = img.resize(scaled_size)

        # Crop as needed
        if scaled_size.x == target_size.x:
            l, r = 0, target_size.x
        else:
            x_center = scaled_size.x/2
            l = int(x_center - target_size.x/2)
            r = int(x_center + target_size.x/2)

        if scaled_size.y == target_size.y:
            u, d = 0, target_size.y
        else:
            y_center = scaled_size.y/2
            u = int(y_center - target_size.y/2)
            d = int(y_center + target_size.y/2)

        img = img.crop((l,u,r,d))
        cimages.append(img)

    try:
        fimg = Image.blend(cimages[0], cimages[1], 0.5)
    except ValueError:
        fimg = cimages[0]

    cimg = find_contours(fimg)
    img = Image.composite(fimg, cimg, cimg.convert('L'))

    buff = io.BytesIO()
    img.convert('RGB').save(buff, format='jpeg')
    return base64.b64encode(buff.getvalue()).decode('utf8')

def find_contours(img):
    img = img.convert('RGB')
    cimg = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(cimg, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 20, 30) # lower threshold, dirtier
    # edges = cv2.Canny(gray, 50, 120) # higher threshold, cleaner
    # edges = cv2.Canny(gray, 60, 120) # higher threshold, cleaner
    edges = cv2.cvtColor(edges, cv2.COLOR_BGR2RGB)
    return Image.fromarray(edges)

