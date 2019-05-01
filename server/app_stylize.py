from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# coding=utf-8

import stylize

import os
import base64
import json
import re
import time
import glob
import shutil
from io import BytesIO
from PIL import Image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template, Response, send_file, make_response
from gevent.pywsgi import WSGIServer
from flask_cors import CORS
from img2midi import convert, call_create_midi, call_play_midi
app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def index():
    return 'style transfer server running'


@app.route('/stylize-with-data', methods=['GET', 'POST'])
def stylize_with_data():
    if request.method == 'POST':
        sessionId = request.form['id']
        styleId = request.form['style']
        highReality = request.form['highReality']
        highQuality = request.form['highQuality']

        userContent = request.form['userContent']
        userStyle = request.form['userStyle']
        contentData = request.form['contentData']
        styleData = request.form['styleData']

        content_size, alpha, adain = get_style_params(highQuality, highReality)
        counter = open("counter").read()
        content_path = './output/pix/'+'pix2pix_image'+counter+'.png'
        style_path = './styles/'+styleId+'.jpg'
        style_out = './output/style/generated_image'+counter+'.png'
        open("counter","w").write(str(int(counter)+1))
        # style_out = './output/style/'+sessionId+'.png'
        open("style", "w").write(styleId)
        if userContent == 'true':
            content_path = './uploads/'+sessionId+'.png'
            image_data = re.sub('^data:image/.+;base64,', '', contentData)
            image_content = Image.open(BytesIO(base64.b64decode(image_data)))
            image_content.save(content_path)

        if userStyle == 'true':
            style_data = re.sub('^data:image/.+;base64,', '', styleData)
            image_style = Image.open(BytesIO(base64.b64decode(style_data)))
            style_path = os.path.join(
                './uploads', '{}_style.png'.format(sessionId))
            image_style.save(style_path)
        stylize.get_stylize_image(
            content_path, style_path, style_out,
            content_size=content_size, alpha=alpha, adain=adain)

        if userStyle == 'true':
            os.remove(style_path)

        with open(os.path.join(os.path.dirname(__file__), style_out), 'rb') as f:
            return u"data:image/png;base64," + base64.b64encode(f.read()).decode('ascii')

    return ''


@app.route('/get-gallery-list', methods=['GET'])
def get_gallery_list():
    galleryDir = './gallery'
    files = [os.path.basename(x) for x in sorted(
        glob.glob(os.path.join(galleryDir, '*.png')), reverse=True)]
    return json.dumps(files)


@app.route('/get-gallery-image/<filename>', methods=['GET'])
def get_gallery_image(filename):
    if os.path.exists('./gallery/'+filename):
        with open('./gallery/'+filename, 'rb') as f:
            return u"data:image/png;base64," + base64.b64encode(f.read()).decode('ascii')
    return ''

@app.route('/get-image', methods=['GET'])
def get_image():
    counter = str(int(open("counter").read()) - 1)
    if os.path.exists('./output/style/generated_image'+counter+'.png'):
        with open('./output/style/generated_image'+counter+'.png', 'rb') as f:
            return u"data:image/png;base64," + base64.b64encode(f.read()).decode('ascii')
    return ''

@app.route('/create-music', methods=['POST'])
def create_music():
    style = str(int(open("style").read()))
    counter = str(int(open("counter").read()) - 1)
    print("chosen style is::",style)
    if os.path.exists('./output/style/generated_image'+counter+'.png'):
        if not os.path.exists('./output/audio/generated_midi' + counter + '.midi'):
            print("file doesn't exist")
            call_create_midi('./output/style/generated_image'+counter+'.png', './output/audio/generated_midi'+counter+'.midi', '../static/generated.midi')
        else:
            print("midi file already exists")
        shutil.copy('./style_audio/' + style + '.mid', '../static/standard.mid', )
        print("midi file copied to static folder")
    return ''

@app.route('/play-music', methods=['POST'])
def play_music():
    counter = str(int(open("counter").read()) - 1)
    if os.path.exists('./output/style/generated_image'+counter+'.png'):
        call_play_midi('./output/audio/generated_midi'+counter+'.midi')
    return ''


@app.route('/submit-to-gallery', methods=['GET', 'POST'])
def submit_to_gallery():
    if request.method == 'POST':
        sessionId = request.form['id']

        style_out = './output/style/'+sessionId+'.png'

        if os.path.isfile(style_out):
            timestr = time.strftime("%Y%m%d-%H%M%S")
            shutil.copy2(style_out, './gallery/'+timestr+'.png')
            return 'True'
        else:
            return 'False'

    return ''


def get_style_params(highQuality, highReality):
    adain = False
    alpha = 0.6
    content_size = 256
    if highReality == 'true':
        adain = True
        alpha = 0.8
    if highQuality == 'true':
        content_size = 512

    return content_size, alpha, adain


if __name__ == '__main__':
    # app.run(port=5002, debug=True)

    # Serve the app with gevent
    print('Start serving style transfer at port 5002...')
    http_server = WSGIServer(('', 5002), app)
    http_server.serve_forever()
