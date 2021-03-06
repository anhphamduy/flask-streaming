#!/usr/bin/env python
from flask import Flask, render_template, Response, request
import socket

# emulated camera
from camera import WebcamVideoStream

import cv2

app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.read()
        ret, jpeg = cv2.imencode('.jpg', frame)

        if camera.stopped:
            break

        # print("after get_frame")
        if jpeg is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
        else:
            print("frame is none")



@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(WebcamVideoStream().start()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    print("Public host: http://" + socket.gethostbyname(socket.gethostname()) + ":5000")
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
