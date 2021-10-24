from flask_cors import CORS
from flask import Flask, send_file, request, jsonify
import os
import random
from xml.dom import minidom
app = Flask(__name__)
CORS(app)


class CaptchaImage:
    def __init__(self, color, filename, svg_path):
        self.color = color
        self.filename = filename
        self.svg_path = svg_path

    def choose_color(self):
        colors = ["green", "black", "blue", "yellow", "brown", "red", "purple", "pink", "orange"]
        self.color = random.choice(colors)

    def choose_svg(self):
        self.filename = random.choice(os.listdir("/home/ruffnorbert/codecool/projects/Balasys/backend/svgs"))
        doc = minidom.parse("/home/ruffnorbert/codecool/projects/Balasys/backend/svgs/" + self.filename)
        path_strings = [path.getAttribute('d') for path
                        in doc.getElementsByTagName('path')]
        doc.unlink()
        self.svg_path = path_strings[0]


captcha = CaptchaImage('red', 'iguana', "")


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/get-captcha-result', methods=['POST'])
def get_captcha_result():
    if request.method == 'POST':
        color_response = request.get_json()["color"]
        image_response = request.get_json()["image"]
        print(captcha.filename)
        print(captcha.color)
        if captcha.filename.find(image_response) != -1 and captcha.color.find(color_response) != -1:
            return jsonify({"response": "OK"})
        else:
            return jsonify({"response": "No match"})


@app.route('/get-captcha-image')
def get_captcha_image():
    captcha.choose_svg()
    return captcha.svg_path


@app.route('/get-captcha-color')
def get_captcha_color():
    captcha.choose_color()
    return captcha.color


if __name__ == '__main__':
    app.run(
        debug=True,
    )
