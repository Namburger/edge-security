from flask import Flask, render_template, Response
from camera.camera import VideoCamera
from detector.detector import Detector
import configparser
import sys

if len(sys.argv) < 2:
    print('Usage:', sys.argv[0], '<config_file>')
    print('Example:', sys.argv[0], 'config/config.cfg')
    exit(0)

app = Flask(__name__)

config = configparser.ConfigParser()
config.read(sys.argv[1])

detector = Detector(config['tflite']['model'], 
        config['tflite'].getboolean('use_edgetpu'))

labels = config['tflite']['labels']
src0 = config['cameras'].getint('src0')
threshold = config['cameras'].getfloat('threshold')

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera(int(src0), threshold, labels, detector)),
        mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True, threaded=True)
